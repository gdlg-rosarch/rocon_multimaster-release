#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_multimaster/hydro-devel/rocon_test/LICENSE
#

##############################################################################
# Imports
##############################################################################

from __future__ import print_function

import os
import sys
import unittest
import rostest.runner
import rocon_utilities
import rospkg
import argparse
from argparse import RawTextHelpFormatter
from rostest.rostestutil import printRostestSummary
import rosunit
from roslaunch.pmon import pmon_shutdown

# Local imports
import loggers
#from loggers import printlog
import runner

##############################################################################
# Methods
##############################################################################


def help_string():
    overview = 'Launches a rocon multi-launch test.\n\n'
    instructions = " \
 - 'rocon-test xxx' : create an empty workspace in ./ecl.\n \
 With some extra info (todo).\n\n \
 "
    return overview + instructions


def _parse_arguments():
    '''
    @raise IOError : if no package name is given and the rocon launcher cannot be found on the filesystem.
    '''
    parser = argparse.ArgumentParser(description=help_string(), formatter_class=RawTextHelpFormatter)
    parser.add_argument('package', nargs='?', default=None, help='name of the package in which to find the test configuration')
    parser.add_argument('test', nargs=1, help='name of the test configuration (xml) file')
    parser.add_argument('-l', '--launch', action='store_true', help='launch each component with rocon_launch [false]')
    parser.add_argument('-p', '--pause', action='store_true', help='pause before tearing down so you can introspect easily [false]')
    parser.add_argument('-s', '--screen', action='store_true', help='run each roslaunch with the --screen option')
    parser.add_argument('-t', '--text-mode', action='store_true', help='log the rostest output to screen rather than log file.')
    args = parser.parse_args()
    # Stop it from being a list (happens when nargs is an integer)
    args.test = args.test[0]
    if args.screen:
        args.screen = "--screen"
    else:
        args.screen = ""
    if not args.package:
        if not os.path.isfile(args.test):
            raise IOError("Test launcher file does not exist [%s]." % args.test)
        else:
            args.package = rospkg.get_package_name(args.test)
    return (args.package, args.test, args.screen, args.pause, args.text_mode)


def test_main():
    (package, name, launch_arguments, pause, text_mode) = _parse_arguments()
    rocon_launcher = rocon_utilities.find_resource(package, name)  # raises an IO error if there is a problem.
    launchers = rocon_utilities.parse_rocon_launcher(rocon_launcher, launch_arguments)
    results_log_name, results_file = loggers.configure_logging(package, rocon_launcher)

    try:
        test_case = runner.create_unit_rocon_test(rocon_launcher, launchers)
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        if pause:
            runner.set_pause_mode(True)
        if text_mode:
            runner.set_text_mode(True)
            result = unittest.TextTestRunner(verbosity=2).run(suite)
        else:
            xml_runner = rosunit.create_xml_runner(package, results_log_name, \
                                         results_file=results_file, \
                                         is_rostest=True)
            result = xml_runner.run(suite)
    finally:
        # really make sure that all of our processes have been killed (should be automatic though)
        test_parents = runner.get_rocon_test_parents()
        for r in test_parents:
            r.tearDown()
        del test_parents[:]
        pmon_shutdown()
    subtest_results = runner.get_results()

    ################################
    # Post stuff
    ################################
    config = rostest.runner.getConfig()
    if config:
        if config.config_errors:
            print("\n[ROCON_TEST WARNINGS]" + '-' * 62 + '\n', file=sys.stderr)
        for err in config.config_errors:
            print(" * %s" % err, file=sys.stderr)
        print('')

    if not text_mode:
        printRostestSummary(result, subtest_results)
        loggers.printlog("results log file is in %s" % results_file)

    # This is not really a useful log, so dont worry about showing it.
    # if log_name:
    #     loggers.printlog("rocon_test log file is in %s" % log_name)

    if not result.wasSuccessful():
        sys.exit(1)
    elif subtest_results.num_errors or subtest_results.num_failures:
        sys.exit(2)
