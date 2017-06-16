__author__ = 'Salvatore Carotenuto of StartupSolutions'


from flask import Flask, render_template, request, Response, jsonify, url_for
from flask_socketio import SocketIO, emit, send
import paho.mqtt.client as mqtt
from threading import Thread
import json
import time
import eventlet
eventlet.monkey_patch()

# our Flask instance
app = Flask(__name__)
app.debug = True

# our SocketIO handler
socketio = SocketIO(app, async_mode=None)

mqtt_client = None


# === Fix for jinja2/angularjs delimiter conflict  =====================================================================

jinja_options = app.jinja_options.copy()

jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>'
))
app.jinja_options = jinja_options


# === MQTT =============================================================================================================


class MQTT_Thread(Thread):
    def __init__(self, mqtt_client):
        print ">>> MQTT_Thread started"
        Thread.__init__(self)
        self.client = mqtt_client
        self.stop = False

    def run(self):
        while not self.stop:
            self.client.loop(timeout=1.0, max_packets=1)
            time.sleep(0.2)

    def terminate(self):
        self.stop = True


# MQTT "on connect" callback: if success, subscribes to needed topics
def on_connect(client, userdata, rc):
    if rc == 0:
        print "Successfully connected to MQTT server. Code:[{0}]".format(str(rc))
        # here, you have to subscribe to all needed topics
        client.subscribe("FRONTEND/#")
        #client.subscribe("WHATEVER/#")
        #client.subscribe("YOUNEED/#")
    elif rc != 0:
        print "Unable to connect to MQTT server. Code:[{0}]".format(str(rc))



# MQTT message handler: when a message is received, sends its content over websocket
#
def on_message(client, userdata, message):
    print ">> [DEBUG] on_message:", client, userdata, message.topic, message.payload
    socketio.emit(message.topic, {'topic': message.topic, 'payload': message.payload})



# === socket.io handling ======================================================================================================


# incoming message handler, for json-encoded payload data
@socketio.on('json')
def handle_socketio_json(json_obj):
    print('### [SOCKET.IO] received JSON: ' + str(json_obj))
    print json_obj
    mqtt_client.publish("USER/REQUEST", json.dumps(json_obj))
    #if json_obj['class'] == 'user_request':
    #    if json_obj['class'] == 'garage_door_open':



@socketio.on('debug')
def handle_display_message(message):
    print('### [SOCKET.IO] received plain message: ' + str(message))



# === Main Routes ======================================================================================================


@app.route('/')
def home():
    return render_template('index.html')


# ======================================================================================================================


def main():
    try:
        global mqtt_client
        mqtt_client = mqtt.Client(client_id="dominomqtt-demo_view_server")
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect("localhost", 1883, 10)
        #
        mqtt_thread = MQTT_Thread(mqtt_client)
        mqtt_thread.start()
        #
        socketio.run(app, host='0.0.0.0', port=5000)
        #
    except Exception, e:
        print "Exception in main:", e
        print "Error:{0} ".format(str(e))


if __name__ == '__main__':
    #
    main()
