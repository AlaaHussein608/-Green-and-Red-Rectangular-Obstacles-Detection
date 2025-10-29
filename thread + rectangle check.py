import cv2
import time
from threading import Thread
import numpy as np

upper_red = np.array([180, 255, 255])
lower_red = np.array([159, 50, 70])
upper_red2 = np.array([9, 255, 255])
lower_red2 = np.array([0, 50, 70])
lower_green = np.array([36, 50, 70])
upper_green = np.array([89, 255, 255])

def is_rectangle(cnt, ratio, Area):
    _, _, w, h = cv2.boundingRect(cnt)
    bbox_area = w * h
    if bbox_area == 0:
        return False
    rectangular_ratio = Area / bbox_area
    return (rectangular_ratio > ratio)


class WebcamStream:
    def __init__(self, stream_id=0):

        self.cap = cv2.VideoCapture(stream_id)
        if self.cap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.cap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is set to False when frames are being read from self.vcap stream
        self.stopped = True
        # reference to the thread for reading next available frame from input stream
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads keep running in the background while the program is executing

    # method for starting the thread for grabbing next available frame in input stream
    def start(self):
        self.stopped = False
        self.t.start()

    # method for reading next frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.cap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
            #time.sleep(0.01) ##################### not used when reading from camera
        self.cap.release()

    # method for returning latest read frame
    def read(self):
        return self.frame.copy()

    # method called to stop reading frames
    def stop(self):
        self.stopped = True


# initializing and starting multi-threaded webcam capture input stream
webcam_stream = WebcamStream(0)
webcam_stream.start()



# processing frames in input stream
while True:
    if webcam_stream.stopped is True:
        break
    else:
        current_frame = webcam_stream.read()

    height = current_frame.shape[0]
    current_frame = current_frame[25:height, :]
    contrast_frame = cv2.convertScaleAbs(current_frame, 1, 2)
    hsv = cv2.cvtColor(contrast_frame, cv2.COLOR_BGR2HSV)

    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask0
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        Area = cv2.contourArea(cnt)
        if Area < 300:
            continue

        if not is_rectangle(cnt, 0.8, Area):    # Rectangle check .........
            continue

        cv2.drawContours(current_frame, [cnt], -1, (0, 0, 255), 2)
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cv2.line(current_frame, (cx, 0), (cx, height), (255, 0, 0), 2)

    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        Area = cv2.contourArea(cnt)
        if Area < 300:
            continue

        if not is_rectangle(cnt, 0.8, Area):    # Rectangle check ..........
            continue

        cv2.drawContours(current_frame, [cnt], -1, (0, 255, 0), 2)
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cv2.line(current_frame, (cx, 0), (cx, height), (255, 0, 0), 2)

    width = current_frame.shape[1]
    left_boundary = int(width / 3)
    right_boundary = int(2 * width / 3)
    cv2.line(current_frame, (left_boundary, 0), (left_boundary, height), (0, 255, 0), 1)
    cv2.line(current_frame, (right_boundary, 0), (right_boundary, height), (0, 255, 0), 1)

    cv2.imshow("Detection", cv2.resize(current_frame, (500, 500)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


webcam_stream.stop()
cv2.destroyAllWindows()
