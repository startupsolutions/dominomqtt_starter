__author__ = 'Salvatore Carotenuto of StartupSolutions'

import paho.mqtt.client as mqtt
import json

# DominoMqtt - Simple helper class, based on paho.mqtt.client
# written by Salvatore Carotenuto of StartupSolutions
#
# based on original code taken from https://pypi.python.org/pypi/paho-mqtt/1.1


class DominoMqtt:

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        #
        self.subscriptions = []
        self.handlers = {}


    # callback for when the client receives a CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for subscription in self.subscriptions:
            client.subscribe(subscription)


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if msg.topic in self.handlers:
            handler = self.handlers[msg.topic]
            if handler:
                handler(msg.payload)


    def connect(self, hostname, port, keepalive):
        self.client.connect(hostname, port=port, keepalive=keepalive)


    def subscribe(self, topic):
        self.subscriptions.append(topic)


    def handler(self, topic, **options):
        def decorator(f):
            self.handlers[topic] = f
            # just for debug
            print "Adding DominoMqtt.handler: ", f
        return decorator


    def publish(self, topic, data=None):
        self.client.publish(topic, str(data) if data else '')


    def publish_as_json(self, topic, data=None):
        self.client.publish(topic, json.dumps(data) if data else '')


    def get_client(self):
        return self.client


    def loop_forever(self):
        self.client.loop_forever()

