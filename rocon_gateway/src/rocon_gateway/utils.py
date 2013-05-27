#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_multimaster/hydro-devel/rocon_gateway/LICENSE
#

##############################################################################
# Imports
##############################################################################

import json
import collections
from gateway_msgs.msg import Rule, ConnectionType

##############################################################################
# Constants
##############################################################################

# for help in iterating over the set of connection constants
connection_types = frozenset([ConnectionType.PUBLISHER, ConnectionType.SUBSCRIBER, ConnectionType.SERVICE, ConnectionType.ACTION_CLIENT, ConnectionType.ACTION_SERVER])
connection_types_list = [ConnectionType.PUBLISHER, ConnectionType.SUBSCRIBER, ConnectionType.SERVICE, ConnectionType.ACTION_CLIENT, ConnectionType.ACTION_SERVER]
connection_type_strings_list = ["publisher", "subscriber", "service", "action_client", "action_server"]
action_types = ['/goal', '/cancel', '/status', '/feedback', '/result']

##############################################################################
# Rule
##############################################################################


class Connection():
    '''
      An object that represents a connection containing all the gory details
      about a connection, allowing a connection to be passed through to a
      foreign gateway

       - rule (gateway_msgs.msg.Rule) (containing type,name,node)
       - type_info              (msg type for pubsub or service api for services)
       - xmlrpc_uri             (the xmlrpc node uri for the connection)
    '''
    def __init__(self, rule, type_info, xmlrpc_uri):
        '''
          @param type_info : either topic_type (pubsub), service api (service) or ??? (action)
          @type string
        '''
        self.rule = rule
        self.type_info = type_info
        self.xmlrpc_uri = xmlrpc_uri

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.rule.type == ConnectionType.SERVICE:
            return '{type: %s, name: %s, node: %s, uri: %s, service_api: %s}' % (self.rule.type, self.rule.name, self.rule.node, self.xmlrpc_uri, self.type_info)
        else:
            return '{type: %s, name: %s, node: %s, uri: %s, topic_type: %s}' % (self.rule.type, self.rule.name, self.rule.node, self.xmlrpc_uri, self.type_info)

    def __repr__(self):
        return self.__str__()


##############################################################################
# Registration
##############################################################################

class Registration():
    '''
      An object that represents a connection registered with the local
      master (or about to be registered). This has all the gory detail
      for the connection. It includes the gateway name it originated
      from as well as master registration information.

       - connection             (the remote connection information)
       - remote_gateway         (the remote gateway from where this connection originated)
       - local_node             (the local anonymously generated node name)
    '''
    def __init__(self, connection, remote_gateway, local_node=None):
        '''
          @param connection : string identifier storing the remote connection details (type, name, node)
          @type gateway_msgs.msg.RemoteRule

          @param remote_gateway : string identifier for where this registration game from
          @type string

          @param local_node : the local node that this registration is created under
          @type string
        '''
        self.connection = connection
        self.remote_gateway = remote_gateway
        self.local_node = local_node

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '[%s]%s' % (self.remote_gateway, format_rule(self.connection.rule))

    def __repr__(self):
        return self.__str__()

##########################################################################
# serialization/deserialization Functions
##########################################################################


def convert(data):
    '''
      Convert unicode to standard string (Not sure how necessary this is)
      http://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    '''
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def serialize(data):
    return json.dumps(data)


def deserialize(str_msg):
    return convert(json.loads(str_msg))


def serialize_connection(connection):
    return serialize([connection.rule.type,
                      connection.rule.name,
                      connection.rule.node,
                      connection.type_info,
                      connection.xmlrpc_uri]
                     )


def deserialize_connection(connection_str):
    deserialized_list = deserialize(connection_str)
    rule = Rule(deserialized_list[0],
                deserialized_list[1],
                deserialized_list[2]
                )
    return Connection(rule, deserialized_list[3], deserialized_list[4])


def serialize_connection_request(command, source, connection):
    return serialize([command, source,
                      connection.rule.type,
                      connection.rule.name,
                      connection.rule.node,
                      connection.type_info,
                      connection.xmlrpc_uri]
                     )


def serialize_rule_request(command, source, rule):
    return serialize([command, source, rule.type, rule.name, rule.node])


def deserialize_request(request_str):
    deserialized_list = deserialize(request_str)
    return deserialized_list[0], deserialized_list[1], deserialized_list[2:]


def get_connection_from_list(connection_argument_list):
    rule = Rule(connection_argument_list[0], connection_argument_list[1], connection_argument_list[2])
    return Connection(rule, connection_argument_list[3], connection_argument_list[4])


def get_rule_from_list(rule_argument_list):
    return Rule(rule_argument_list[0], rule_argument_list[1], rule_argument_list[2])

##########################################################################
# Regex
##########################################################################


def is_all_pattern(pattern):
    '''
      Convenience function for detecting the 'all' pattern.

      @param pattern : the name rule string for the flip all concept
      @type str
      @return true if matching, false otherwise
      @rtype Bool
    '''
    if pattern == ".*":
        return True
    else:
        return False


##########################################################################
# Formatters
##########################################################################

def format_rule(rule):
    return '[%s][%s][%s]' % (rule.type, rule.name, rule.node)

##########################################################################
# Factories
##########################################################################


def create_empty_connection_type_dictionary():
    '''
      Used to initialise a dictionary with rule type keys
      and empty lists.
    '''
    dic = {}
    for connection_type in connection_types:
        dic[connection_type] = []
    return dic
