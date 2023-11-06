import cv2
import numpy as np
print(cv2.__version__)
camSet0 = 'nvarguscamerasrc sensor-id=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=360, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.15 saturation=1.2 ! appsink'
cam0 = cv2.VideoCapture(camSet0,cv2.CAP_GSTREAMER)
camSet1 = 'nvarguscamerasrc sensor-id=1 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=0 ! video/x-raw, width=640, height=360, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.15 saturation=1.2 ! appsink'
cam1 = cv2.VideoCapture(camSet1,cv2.CAP_GSTREAMER)
while True:
    _,frame0 = cam0.read()
    # cv2.imshow('myCam0',frame0)

    _,frame1 = cam1.read()
    # cv2.imshow('myCam1',frame1)

    camera_images = np.hstack((frame1, frame0)) 
    
    cv2.imshow('myCam1',camera_images)

    if cv2.waitKey(1)==ord('q'):
        break

cam0.release()
cam1.release()
cv2.destroyAllWindows()
