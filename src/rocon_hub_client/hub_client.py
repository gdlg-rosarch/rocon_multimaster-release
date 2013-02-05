#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_multimaster/master/rocon_hub_client/LICENSE
#
##############################################################################
# Imports
##############################################################################

import rospy
import redis
from .hub_connector import HubConnector


class HubClient(HubConnector):

    # HubConnector provide
    #    connect(hub_uri)

    ConnectionError = redis.exceptions.ConnectionError

    pool = None
    server = None
    pubsub = None
    callback = None
    namespace = ''
    param = {}

    def __init__(self, whitelist, blacklist, is_zeroconf, namespace, name, callbacks):
        super(HubClient, self).__init__(whitelist, blacklist, is_zeroconf, self._connectToHub)

        self._namespace = namespace
        self._name = name
        self._unique_name = ''
        self._callbacks = callbacks

        self._redis_keys = {}
#        self._redis_keys['index'] = createHubKey('index')
        self._redis_channels = {}
        self._redis_pubsub_server = None

    def _connectToHub(self, ip, portarg):
        try:
            self.pool = redis.ConnectionPool(host=ip, port=portarg, db=0)
            self.server = redis.Redis(connection_pool=self.pool)
            rospy.logdebug("HubClient : connected to the hub's redist server.")
            self._redis_pubsub_server = self.server.pubsub()
        except redis.exceptions.ConnectionError as unused_e:
            rospy.logerror("HubClient : failed rule to the hub's redis server.")
            return False
            raise
        return True

    def registerKey(self, key, element):
        key = self._namespace + ":" + key
        element = self._namespace + ":" + element

        if self.server.sadd(key, element):
            return True
        else:
            raise Exception("Same concertmaster name exist")
            return False

    def unregisterKey(self, key, element):
        try:
            key = self._namespace + ":" + key
            element = self._namespace + ":" + element
            self.server.srem(key, element)
        except redis.exceptions.ConnectionError:
            raise  # ~HubClient.ConnectionError

    def getValues(self, key):
        key = self._namespace + ":" + key
        values = self.server.smembers(key)

        values = [v[len(self._namespace) + 1:] for v in values]
        return values
