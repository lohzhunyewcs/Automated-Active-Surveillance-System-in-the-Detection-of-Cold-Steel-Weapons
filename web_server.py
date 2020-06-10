import zmq
import json
import base64
from flask import Flask, flash, render_template, Response, stream_with_context, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
import cv2
import os
from datetime import datetime
import numpy as np

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

app = Flask(__name__)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index', methods=["GET", "POST"])
def dropdown():
    if request.method == "POST":
        req = request.form
        camera = req["camera"]
        print(camera)

        sock_send.send_multipart([str.encode(PORT2), str.encode(camera)])
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(gen()), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    PORT = "5555"
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://localhost:{}".format(PORT))
    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)

    # Socket can be subscribed to multiple PUB
    sock.subscribe(b"key1")
    #img_array to store the frames which will be accessed later once there's a knife detected.
    # If knife detected, then for loop access each frame, then it will merge all the frames and create a video
    # if knife is no longer detected.
    img_array = []
    knife_detected = []
    prev_state = False
    while True:
        # Receive frame
        # evt = poller.poll(100)
        # if evt:
        [_, json_data] = sock.recv_multipart()
        data = json.loads(json_data)
        knife = data['knife']
        print(f'knife: {knife}, type(knife): {type(knife)}')
        if knife:
            print('confirmed knife detected')
            socketio.emit("knife detected", {'status': 'success'}, broadcast=True)
        frame = base64.decodebytes(bytes(data['frame'], 'UTF-8'))
        
        #knife is detected
        if knife:
            print("reach here")
            if not prev_state:
                prev_state = knife
            #start recording
            timestamp = datetime.now()
            nparr = np.fromstring(frame, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            height, width, layers = img_np.shape
            size = (width, height)
            img_array.append(img_np)
        #knife is not detected
        else:
            print("reach here 2")
            if prev_state:
                print('writing video')
                #stop recording
                timestamp2 = datetime.now()
                vid_name = timestamp.strftime("%d-%m-%Y_%I-%M-%S") + timestamp2.strftime("_%I-%M-%S") + ".mp4"
                vid_name = vid_name.replace(':', '-')
                vid_name2 = "project.mp4"
                # out = cv2.VideoWriter(vid_name2, get_video_type(vid_name), 30, size)
                print(vid_name)
                #out = cv2.VideoWriter(vid_name, cv2.VideoWriter_fourcc(*'XVID'), 5, size)
                # for i in range(len(img_array)):
                #     out.write(img_array[i])
                #out.release()
                img_array = []
                prev_state = False
        # Display
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # else:
        #     yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'b'\r\n')


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    knife_detected = [False]
    PORT = "5555"
    PORT2 = "5556"

    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://localhost:{}".format(PORT))
    sock.subscribe(str.encode(PORT))

    sock_send = context.socket(zmq.PUB)
    sock_send.bind("tcp://*:{}".format(PORT2))

    app.debug = True
    app.config['SECRET_KEY'] = 'secretkey'
    app.run(host='localhost', port=5001, use_reloader = False)
