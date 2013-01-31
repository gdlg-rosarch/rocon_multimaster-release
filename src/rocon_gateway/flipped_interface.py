#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_multimaster/master/rocon_gateway/LICENSE
#

##############################################################################
# Imports
##############################################################################

from gateway_msgs.msg import Rule, RemoteRule, ConnectionType
import copy
import re

# Local imports
import utils
import interactive_interface

##############################################################################
# Flipped Interface
##############################################################################


class FlippedInterface(interactive_interface.InteractiveInterface):
    '''
      The flipped interface is the set of rules
      (pubs/subs/services/actions) and rules controlling flips
      to other gateways.
    '''
    def __init__(self, firewall, default_rule_blacklist, default_rules, all_targets):
        '''
          Initialises the flipped interface.

          @param firewall : flag to prevent this gateway from accepting flips
          @type Bool
          @param default_rule_blacklist : used when in flip all mode
          @type dictionary of gateway
          @param default_rules : static rules to flip on startup
          @type gateway_msgs.msg.RemoteRule[]
          @param all_targets : static flip all targets to flip to on startup
          @type string[]

        '''
        interactive_interface.InteractiveInterface.__init__(self, default_rule_blacklist, default_rules, all_targets)

        self.firewall = firewall

        # Function aliases
        self.flipped = self.active
        self.flip_all = self.add_all
        self.unflip_all = self.remove_all

    ##########################################################################
    # Monitoring
    ##########################################################################

    def update(self, connections, gateways,unique_name):
        '''
          Computes a new flipped interface and returns two dictionaries -
          removed and newly added flips so the watcher thread can take
          appropriate action (inform the remote gateways).

          This is run in the watcher thread (warning: take care - other
          additions come from ros service calls in different threads!)

          @param connections : list of all the system state connections from the local master
          @type connection type keyed dictionary of utils.Connection lists.

          @param gateways : gateways that are available (registered on the hub)
          @type string

          @return new_flips, old_flips
          @rtype pair of connection type keyed dictionary of gateway_msgs.msg.Rule lists.
        '''
        # SLOW, EASY METHOD

        flipped = utils.createEmptyConnectionTypeDictionary()
        new_flips = utils.createEmptyConnectionTypeDictionary()
        removed_flips = utils.createEmptyConnectionTypeDictionary()
        diff = lambda l1,l2: [x for x in l1 if x not in l2]  # diff of lists
        self._lock.acquire()
        # Prune flips that are not in the gateway list anymore, keep the rules though
        for connection_type in utils.connection_types:
            self.flipped[connection_type] = [flip for flip in self.flipped[connection_type] if flip.gateway in gateways]
        # Totally regenerate a new flipped interface, compare with old
        for connection_type in connections:
            for connection in connections[connection_type]:
                flipped[connection_type].extend(self._generate_flips(connection.rule.type, connection.rule.name, connection.rule.node, gateways,unique_name))
            new_flips[connection_type] = diff(flipped[connection_type],self.flipped[connection_type])
            removed_flips[connection_type] = diff(self.flipped[connection_type],flipped[connection_type])
        self.flipped = copy.deepcopy(flipped)
        self._lock.release()
        return new_flips, removed_flips
        
        # OPTIMISED METHOD
        #   Keep old rule state and old flip rules/patterns around
        #
        #   1 - If flip rules/patterns disappeared [diff(old_rules,new_rules)]
        #         Check if the current flips are still valid
        #         If not all are, remove and unflip them
        #
        #   2 - If rules disappeared [diff(old_conns,new_conns)]
        #         If matching any in flipped, remove and unflip
        #
        #   3 - If flip rules/patterns appeared [diff(new_rules,old_rules)]
        #         parse all conns, if match found, flip
        #
        #   4 - If rules appeared [diff(new_conns,old_conns)]
        #         check for matches, if found, flou
        #
        # diff = lambda l1,l2: [x for x in l1 if x not in l2] # diff of lists

    ##########################################################################
    # Utility Methods
    ##########################################################################

        
    def _generate_flips(self, type, name, node, gateways,unique_name):
        '''
          Checks if a local rule (obtained from master.getSystemState) 
          is a suitable association with any of the rules or patterns. This can
          return multiple matches, since the same local rule 
          properties can be multiply flipped to different remote gateways.
            
          Used in the update() call above that is run in the watcher thread.
          Note, don't need to lock here as the update() function takes care of it.
          
          @param type : rule type
          @type str : string constant from gateway_msgs.msg.Rule
          
          @param name : fully qualified topic, service or action name
          @type str
          
          @param node : ros node name (coming from master.getSystemState)
          @type str

          @param gateways : gateways that are available (registered on the hub)
          @type string
          
          @return all the flip rules that match this local rule
          @return list of RemoteRule objects updated with node names from self.watchlist
        '''
        matched_flip_rules = []
        for flip_rule in self.watchlist[type]:
            # Check if the flip rule corresponds to an existing gateway
            matched_gateways = []
            for gateway in gateways:
                gateway_match_result = re.match(flip_rule.gateway, gateway)
                if gateway_match_result and gateway_match_result.group() == gateway:
                    matched_gateways.append(gateway)
            if not matched_gateways:
                continue

            # Check names
            rule_name = flip_rule.rule.name
            matched = self.is_matched(flip_rule,rule_name,name,node)

            if not matched:
                rule_name = '/' + unique_name + '/' + flip_rule.rule.name
                matched = self.is_matched(flip_rule,rule_name,name,node)

            if not matched: 
                rule_name = '/' + flip_rule.rule.name
                matched = self.is_matched(flip_rule,rule_name,name,node)

            if matched:
                for gateway in matched_gateways:
                    matched_flip = copy.deepcopy(flip_rule)
                    matched_flip.gateway = gateway # just in case we used a regex
                    matched_flip.rule.name = name  # just in case we used a regex
                    matched_flip.rule.node = node  # just in case we used a regex
                    matched_flip_rules.append(matched_flip)
        return matched_flip_rules
    
    ##########################################################################
    # Accessors for Gateway Info
    ##########################################################################

    def get_flipped_connections(self):
        '''
          Gets the flipped connections list for GatewayInfo consumption.
          
          @return the list of flip rules that are activated and have been flipped.
          @rtype RemoteRule[]
        '''
        flipped_connections = []
        for connection_type in utils.connection_types:
            flipped_connections.extend(copy.deepcopy(self.flipped[connection_type]))
        return flipped_connections
    
    
if __name__ == "__main__":
    
    gateways = ['dude','dudette']
    dudes = ['fred', 'dude']
    dudes[:] = [x for x in dudes if x in gateways]
    print dudes
