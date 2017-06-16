__author__ = 'Salvatore Carotenuto of StartupSolutions'

import sys                  # needed to import stuff from relative path
sys.path.append('..')

from dominomqtt import DominoMqtt
from datetime import datetime
import json
import time


# ----------------------------------------------------------------------------------------------------------------------

# 1: create your DominoMqtt instance 
domino = DominoMqtt()


# 2: add topic subscriptions to your DominoMqtt instance
# note: all topics are user defined
domino.subscribe('SENSORDATA/#') # subscribes all topics starting with SENSORDATA/
domino.subscribe('USER/#')
#domino.subscribe('WHATEVER/#')
#domino.subscribe('YOUNEED/#')


# 3: define your topic handlers, using a function decorator:

@domino.handler('SENSORDATA/TEMPERATURE')
def sensordata_temperature_handler(data):
    #
    # note: is up to you to parse the incoming message payload
    # In this case, we are assuming that this topic will receive
    # payloads in json format
    #
    payload = json.loads(data)
    print "[sensordata_temperature_handler] received:", payload
    #
    #
    # ...do whatever you want with the received data...
    # i.e.: check if values are out of range
    if payload['temperatures']['bedroom'] > 20:
        # in this case we are publishing a plain text message
        domino.publish('FRONTEND/EVENT/WARNING', 'Hot temperature in bedroom!!!')
    #
    #
    # then, you can (re)publish everything you need on running MQTT server instance:
    #
    # in this case we are publishing the content of a dict, in json format:
    domino.publish_as_json('FRONTEND/TEMPERATURE/UPDATE', payload)


@domino.handler('SENSORDATA/PRESENCE')
def sensordata_presence_handler(data):
    #
    # note: is up to you to parse the incoming message payload
    # In this case, we are assuming that this topic will receive
    # payloads in json format
    #
    payload = json.loads(data)
    print "[sensordata_presence_handler] received:", payload
    #
    #
    # ...do whatever you want with the received data...
    #
    # then, you can (re)publish everything you need on running MQTT server instance:
    #
    # in this case we are publishing the content of received dict (payload),
    # in json format, without modifications, but on another topic:
    domino.publish_as_json('FRONTEND/EVENT/ALERT', payload)


@domino.handler('USER/REQUEST')
def user_request_handler(data):
    #
    # note: is up to you to parse the incoming message payload
    # In this case, we are assuming that this topic will receive
    # payloads in json format
    #
    payload = json.loads(data)
    print "[user_request_handler] received:", payload
    #
    #
    # ...do whatever you want with the received data...
    #
    # in this case, we are parsing user requests incoming from view server's frontend page
    # (see handle_socketio_json handler in view_server.py)
    #
    if payload['class'] == 'user_request':
        if payload['data'] == 'garage_door_open':
            #
            # assume you process "physically" the request here
            # i.e.: on {"class": "user_request", "data": "garage_door_open"}, open the garage door
            #
            payload['class'] = 'action_done'
            payload['item'] = 'garage_door'
            payload['status'] = 'open'
            #
            domino.publish_as_json('FRONTEND/STATUS/UPDATE', payload)
        #
        elif payload['data'] == 'garage_door_close':
            #
            # assume you process "physically" the request here
            # i.e.: on {"class": "user_request", "data": "garage_door_open"}, open the garage door
            #
            payload['class'] = 'action_done'
            payload['item'] = 'garage_door'
            payload['status'] = 'closed'
            #
            domino.publish_as_json('FRONTEND/STATUS/UPDATE', payload)


# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    try:
        # does connection to running mosquitto broker
        domino.connect("localhost", port=1883, keepalive=60)
        #
        print "Starting..."
        domino.loop_forever()
        #
    except Exception as e:
        print "Error: exception in main. Cause:", e

