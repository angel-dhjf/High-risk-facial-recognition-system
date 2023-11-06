import cv2
import numpy as np
import fuzzy,faceRec,rec_black
from csi_camera import CSI_Camera
import os

show_fps = True
    
# Simple draw label on an image; in our case, the video frame
def draw_label(cv_image, label_text, label_position):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (255,255,255)
    # You can get the size of the string with cv2.getTextSize here
    cv2.putText(cv_image, label_text, label_position, font_face, scale, color, 1, cv2.LINE_AA)

# Read a frame from the camera, and draw the FPS on the image if desired
# Return an image
def read_camera(csi_camera,display_fps):
    _ , camera_image=csi_camera.read()
    if display_fps:
        draw_label(camera_image, "Frames Displayed (PS): "+str(csi_camera.last_frames_displayed),(10,20))
        draw_label(camera_image, "Frames Read (PS): "+str(csi_camera.last_frames_read),(10,40))
    return camera_image

# Good for 1280x720
DISPLAY_WIDTH=640
DISPLAY_HEIGHT=360
# For 1920x1080
# DISPLAY_WIDTH=960
# DISPLAY_HEIGHT=540

# 1920x1080, 30 fps
SENSOR_MODE_1080=2
# 1280x720, 60 fps
SENSOR_MODE_720=3

def start_cameras():
    HAAR_CASCADE_XML_FILE_FACE = "haarcascades/haarcascade_frontalface_alt2.xml"
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_XML_FILE_FACE)

    left_camera = CSI_Camera()
    left_camera.create_gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=SENSOR_MODE_720,
            framerate=30,
            flip_method=2,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
    left_camera.open(left_camera.gstreamer_pipeline)
    left_camera.start()

    right_camera = CSI_Camera()
    right_camera.create_gstreamer_pipeline(
            sensor_id=1,
            sensor_mode=SENSOR_MODE_720,
            framerate=30,
            flip_method=2,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
    right_camera.open(right_camera.gstreamer_pipeline)
    right_camera.start()
    


    cv2.namedWindow("CSI Cameras", cv2.WINDOW_AUTOSIZE)

    if (not left_camera.video_capture.isOpened() or not right_camera.video_capture.isOpened()):
        print("Unable to open any cameras")
        SystemExit(0)
    try:
        # Start counting the number of frames read and displayed
        left_camera.start_counting_fps()
        right_camera.start_counting_fps()

        while cv2.getWindowProperty("CSI Cameras", 0) >= 0 :

            rightimg=read_camera(right_camera,False)
            outgrayscale_image = cv2.cvtColor(rightimg, cv2.COLOR_BGR2GRAY)
            outdetected_faces = face_cascade.detectMultiScale(outgrayscale_image, 1.3, 5)
            for (x_pos, y_pos, width, height) in outdetected_faces:
                # cv2.rectangle(frameOut, (x_pos, y_pos), (x_pos + width, y_pos + height), (0, 255, 0), 2)
                cropout = rightimg[y_pos - 20:y_pos + height + 20, x_pos - 20:x_pos + width + 20]
                if fuzzy.fuzzycritical(cropout):
                    faceRec.faceRec(cropout,0)
                    rec_black.faceRec(cropout,0)
                    try:
                        cv2.imshow("cropout", cropout)
                    except:
                        pass
            leftimg=read_camera(left_camera,False)
            ingrayscale_image = cv2.cvtColor(leftimg, cv2.COLOR_BGR2GRAY)
            indetected_faces = face_cascade.detectMultiScale(ingrayscale_image, 1.3, 5)
            for (x_pos, y_pos, width, height) in indetected_faces:
                # cv2.rectangle(frameIcn, (x_pos, y_pos), (x_pos + width, y_pos + height), (0, 255, 0), 2)
                cropin = leftimg[y_pos - 20:y_pos + height + 20, x_pos - 20:x_pos + width + 20]
                if fuzzy.fuzzycritical(cropin):
                    faceRec.faceRec(cropin,1)
                    rec_black.faceRec(cropin,1)
                    try:
                        cv2.imshow("cropin", cropin)
                        
                    except:
                        pass


            left_image=read_camera(left_camera,show_fps)
            right_image=read_camera(right_camera,show_fps)
            
            camera_images = np.hstack((left_image, right_image))
            cv2.imshow("CSI Cameras", camera_images)
            left_camera.frames_displayed += 1
            right_camera.frames_displayed += 1

            if (cv2.waitKey(5) & 0xFF) == 27:
                break   

    finally:
        left_camera.stop()
        left_camera.release()
        right_camera.stop()
        right_camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_cameras()
