import base64

import cv2
import os
import io
import PIL.Image as Image

from array import array

import numpy as np


def object_recognition(img):
    #img = cv2.imread('lena.PNG')
    #cap = cv2.VideoCapture(0)
    #cap.set(3, 640)
    #cap.set(4, 480)

    classNames = []
    classFile = 'coco.names'
    with open(classFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    # while True:
    #     success, img = cap.read()
    #     classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    #     print(classIds, confs, bbox)
    #     if len(classIds) != 0:
    #         for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
    #             cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
    #             cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    #             cv2.putText(img, str(confidence), (box[0] + 10, box[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 255, 0), 2)
    #     cv2.imshow("Output", img)
    #     cv2.waitKey(1)

    # #print(img)
    # nparr = np.fromstring(img, np.uint8)
    # #nparr.tofile("output.txt", sep="", format="")
    # print("NPARR: ")
    # print(nparr)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # print("IMDECODE: ")
    # print(img)

    imgdata = base64.b64decode(str(img))
    image = Image.open(io.BytesIO(imgdata))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    ##Rescale, hogy ne lassítsa a gépet
    #img2 = cv2.resize(img, dsize=(160, 80), interpolation=cv2.INTER_CUBIC)

    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    print(classIds, confs, bbox)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, str(confidence), (box[0] + 10, box[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 255, 0), 2)
    #cv2.imshow("Output", img2)
    #cv2.waitKey(1)

    pil_img = Image.fromarray(img)
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    return new_image_string
