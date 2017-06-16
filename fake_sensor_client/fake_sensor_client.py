__author__ = 'Salvatore Carotenuto of StartupSolutions'

import sys                  # needed to import stuff from relative path
sys.path.append('..')

from dominomqtt import DominoMqtt
from threading import Thread
from random import randint
import time


# ----------------------------------------------------------------------------------------------------------------------

# DominoMqtt instance
domino = DominoMqtt()

# ----------------------------------------------------------------------------------------------------------------------

class PublisherThread(Thread):
    def __init__(self, dominoMqttInstance):
        print ">>> PublisherThread started"
        Thread.__init__(self)
        self.domino = dominoMqttInstance
        self.stop = False

    def randomTemperature(self, min, max):
        return randint(min*10, max*10) / 10.0

    def run(self):
        while not self.stop:
            time.sleep(4)
            #
            data = {'temperatures': {}}
            # for each of these areas, generates a rendom temperature between 16 and 34 degrees (including decimals)
            data['temperatures']['kitchen']    = self.randomTemperature(16, 34)
            data['temperatures']['livingroom'] = self.randomTemperature(16, 34)
            data['temperatures']['bedroom']    = self.randomTemperature(16, 34)
            data['temperatures']['bathroom']   = self.randomTemperature(16, 34)
            data['temperatures']['garage']     = self.randomTemperature(16, 34)
            #
            print "publishing..."
            self.domino.publish_as_json('SENSORDATA/TEMPERATURE', data)
            #
            # simulates fake human presence in garage area
            val = randint(1, 1000)
            if val > 500:
                print "sending fake human presence detection..."
                self.domino.publish_as_json('SENSORDATA/PRESENCE', { 'areas': ['garage'] })

    def terminate(self):
        self.stop = True


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    try:
        # does connection to running mosquitto broker
        domino.connect("localhost", port=1883, keepalive=60)
        #
        # starts fake publisher thread
        publisher_thread = PublisherThread(domino)
        publisher_thread.setDaemon(True)
        publisher_thread.start()
        #
        print "Starting..."
        domino.loop_forever()
        #
    except Exception as e:
        print "Error: exception in main. Cause:", e
