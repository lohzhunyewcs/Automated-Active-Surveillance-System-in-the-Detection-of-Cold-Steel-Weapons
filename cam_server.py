import zmq
import json
import base64
import cv2
# import slack
import datetime
from dl_models.driver import yolov3, yolo_predict

if __name__ == '__main__':
    # app.debug = True
    # app.run(host='localhost', port=5000)

    PORT = "5555"
    # SLACK_BOT_USER_TOKEN='xoxb-1008563764053-1135041192726-BmfcvU2h0zjMkeh6nph07zHD'
    SLACK_BOT_USER_TOKEN='xoxb-1150026834819-1150038591571-MivgMsLbDG2XcDfNFzhIGicR'
    detected = [True, False]
    # Setup publisher
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind("tcp://*:{}".format(PORT))

    # # Create a SlackClient for your bot to use for Web API requests
    # slack_bot_token = SLACK_BOT_USER_TOKEN
    # Client = slack.WebClient(slack_bot_token)

    # Yolo Model
    yolo_model, opt = yolov3(linux=False)


    # vc = cv2.VideoCapture(0)
    vc = cv2.VideoCapture('data/demo_video/MVI_3258(edited).mp4')
    if not vc.isOpened():
        raise Exception()
    # while True:
    while vc.isOpened():
        _, img = vc.read()
        # frame = open("termi.jpg", 'rb').read()
        img = cv2.resize(img, (1020, 1020))
        got_knife = True
        # img, got_knife = yolo_predict(yolo_model, opt, image=img, to_read_img=False)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        # Process frame
        # -------------------------------------------------------

        # if detected[0] != detected[1]:
        #     if detected[0]:
        #         Client.chat_postMessage(channel="C014DQ23Q8J",
        #                                 text='Knife detection start: '+datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        #     else:
        #         Client.chat_postMessage(channel="C014DQ23Q8J",
        #                                 text='Knife detection end: '+datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        # # Update detected
        # detected[1] = detected[0]
        # detected[0] = True

        data = json.dumps({
            "frame": base64.encodebytes(frame).decode("utf-8"),
            "knife": got_knife
        })
        # Send processed frame to model
        sock.send_multipart([b"key1", bytes(data,"UTF-8")])
        # topic = random.randrange(9999,10005)
        # messagedata = random.randrange(1,215) - 80
        # sock.send_string("%d %s" % (10001, str(data)))
        # print("Sent "+str(base64.encodebytes(frame).decode("utf-8")))
