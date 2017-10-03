# dominomqtt_starter
A simple, complete starter project for DominoMQTT architecture.

DominoMQTT is a simple architecture based on Python, Flask, MQTT, Socket.io and AngularJS, with a bit of custom "glue" code, and good intentions.

### Preface
Necessity is the mother of all inventions. I often work on projects based on Flask and REST APIs, with a strong focus on user experience, given by AngularJS. So, for a quite recent project, I needed somewhat more *reactive*. Somewhat that cannot be done with the classic HTTP GET/POST mechanisms, and long pollings. And, I forgot to mention that the project I was working on is somewhat like an *IoT application*, for temperature control in a small-industry production process.
So, I decided to write a my own architecure, taking state-of-the-art components (MQTT, Mosquitto, Python, Flask, Socket.io and AngularJS) and glueing them via a simple class I wrote, **DominoMQTT**.

### The code
The code is very light, making it possible to run it also on small machines, such as embedded GNU/Linux devices. Actually I run this code, in production mode, on RaspberryPi and OrangePi single-board computers.

**Note:** all the code of this project needs a running Mosquitto (MQTT Broker) instance.

This project is split across three subprojects:
- **logic_worker**: the place where all application logic happens. This is a MQTT client, and the main component of the architecture;
- **view_server**: another MQTT client. A Flask / Socket.IO / AngularJS application that presents a web interface to the user, on default port 5000;
- **fake_sensor_client**: a third MQTT client. As the name says, a fake "sensor" application that sends fake data to the running Mosquitto instance. In production, this code is replaced (for my projects) by dedicated hardware boards and real sensors; 

As you can see, *DominoMQTT* is a common package required by *logic_worker* and *fake_sensor_client* subprojects.

### Quickstart
- install and run Mosquitto, e.g. on Debian/Ubuntu:
```
    $ sudo apt-get install mosquitto
    $ sudo -i
    # mosquitto -v
```
- clone locally this project (e.g. $ git clone https://github.com/startupsolutions/dominomqtt_starter.git);
- view the file *system_architecture.pdf*, to see (briefly) how it works;
- inspect the code: start looking at **logic_worker** subproject: here is where you can implement all your business logic. In the code, you can find some very clear comments on how you can edit the code to suit your needs. Then move on **view_server** subproject, to see how to implement message handling. See python and angularjs code;
- create a Python 2 virtualenv and "pip install" required packages for every project: you can find a *requirements.txt* for every subproject. So in each subfolders: logic_worker, view_server, fake_sensor_client do:
          $ pip install -r requirements.txt
- start a **Mosquitto** instance on your machine (i.e.: mosquitto -v);
- start a **logic_worker** instance (python logic_worker.py);
- start a **view_server** instance (python view_server.py);
- start a **fake_sensor_client** instance (python fake_sensor_client.py);
- open your web browser on http://localhost:5000;
- enjoy!

For every request, you can write me at carotenuto@startupsolutions.it
