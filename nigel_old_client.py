import zmq
import json
import base64
import cv2
import os
import numpy as np
from datetime import datetime
from flask import Flask, flash, render_template, Response, stream_with_context, redirect, request, url_for

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


@app.route('/')
def index():
    # flash("hello")
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(gen()), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    PORT = "5555"
    prev_state = False
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://localhost:{}".format(PORT))

    #out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    # topicfilter = "10001"
    # sock.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

    # Socket can be subscribed to multiple PUB
    sock.subscribe(b"key1")
    #img_array to store the frames which will be accessed later once there's a knife detected.
    # If knife detected, then for loop access each frame, then it will merge all the frames and create a video
    # if knife is no longer detected.
    img_array = []
    while True:
        # Receive frame
        [_, json_data] = sock.recv_multipart()
        data = json.loads(json_data)
        knife_detected[0] = data['knife']
        print(knife_detected[0])
        frame = base64.decodebytes(bytes(data['frame'], 'UTF-8'))
        #knife is detected
        if knife_detected[0] == True:
            print("reach here")
            if prev_state == False:
                prev_state = knife_detected[0]
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
            if prev_state == True:
                #stop recording
                timestamp2 = datetime.now()
                vid_name = timestamp.strftime("%d/%m/%Y_%I:%M:%S") + timestamp2.strftime("_%I:%M:%S") + ".mp4"
                vid_name2 = "project.mp4"
                # out = cv2.VideoWriter(vid_name2, get_video_type(vid_name), 30, size)

                out = cv2.VideoWriter(vid_name2, cv2.VideoWriter_fourcc(*'XVID'), 5, size)
                for i in range(len(img_array)):
                    out.write(img_array[i])
                out.release()
                img_array = []
                prev_state = False


        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')







@app.route('/getbool')
def getbool():
    def events():
        PORT = "5555"
        context = zmq.Context()
        sock = context.socket(zmq.SUB)
        sock.connect("tcp://localhost:{}".format(PORT))
        sock.subscribe(b"key1")
        [_, json_data] = sock.recv_multipart()
        data = json.loads(json_data)
        knife = str(data['knife'])
        yield "%s" % ("bananan")
    return Response(events(), content_type='text/event-stream')


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    knife_detected = [False]
    app.debug = True
    app.config['SECRET_KEY'] = 'secretkey'
    app.run(host='localhost', port=5001)
