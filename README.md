# Automated-Active-Surveillance-System-in-the-Detection-of-Cold-Steel-Weapons
In our final year project, we will be creating a website that will be able to provide and automatic real-time detection of cold steel weapon. In the event of a detection, the system will then alert the user through the website

We will be testing at least 4 of the following networks to detect the cold steel weapons:
1) YOLOV3-spp
2) YOLACT
3) CenterNet
4) CenterMask2

We have made our own dataset of cold steel weapons and will be using it as a factor in determining which networks we will use.

## Dependencies
We recommend using `pip` to install the necessary Python modules.
Command for installing dependencies below are prefixed with `pip install`:
  * Flask 
  * opencv-python
  * Slack
  * Slack-client
  * imagezmq
  * zmq
  * requests
  * Flask-SocketIO
  * click
  * image-io
  * itsdangerous
  * Jinja2
  * MarkupSafe
  * numpy
  * Pillow
  * python-engineio
  * python-socketio
  * pyzmq
  * six
  * Werkzeug
  * flask_bootstrap

## Starting the web app
 python web_server.py
 python client_server.py

## Alternative method of setting up (MAC/ Linux)
```
./start.sh
```
If any permission problems are encountered, run this command to allow it to be executable
```
chmod +x setup_all.sh
```

##Alternative method of setting up (Windows)
Run start_servers.bat

You will be able to access the web app on your localhost:5555 after running the commands

The code and dataset will be released when the project is over. 
