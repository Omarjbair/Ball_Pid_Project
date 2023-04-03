# import library

import cv2
import numpy as np
import serial


# start class
class Ball:

    # constructor function
    def __init__(self):
        self.exposure = None
        self.min_h = None
        self.max_h = None
        self.lower = None
        self.upper = None
        self._ = None
        self.frame = None
        self.hsv = None
        self.mask = None
        self.black = None
        self.kernel = None
        self.contours = None
        self.no_use = None
        self.masking_ball = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.angle = 0
        self.saturation = 0
        self.value = 0
        self.stop = 0
        self.var = 100
        # self.trackbar_name = "trackbar_ball"
        self.vid = cv2.VideoCapture(2)
        self.arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

    # Do_nothing function
    def nothing(self):
        pass

    # create trackbar
    # def hue_trackbar(self):
    #     cv2.namedWindow(self.trackbar_name)
    #     cv2.createTrackbar("min_h", self.trackbar_name, 0, 180, self.nothing)
    #     cv2.createTrackbar("max_h", self.trackbar_name, 0, 180, self.nothing)
    # frame function
    def Frame_detect(self):
        _, self.frame = self.vid.read()
        # self.frame = cv2.flip(self.frame, 1)
        self.frame = cv2.GaussianBlur(self.frame, (21, 21), 0)
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # self.min_h = cv2.getTrackbarPos("min_h", self.trackbar_name)
        # self.max_h = cv2.getTrackbarPos("max_h", self.trackbar_name)
        lower_saturation = self.hsv[:, :, 1]
        lower_value = self.hsv[:, :, 2]
        self.value = np.average(lower_value)
        self.saturation = np.average(lower_saturation)
        self.lower = np.array([30, int(self.saturation), int(self.value)])
        self.upper = np.array([90, 255, 255])
        # self.vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        self.vid.set(17, -7)

    # masking function
    def masking(self):
        self.Frame_detect()
        self.mask = cv2.inRange(self.hsv, self.lower, self.upper)
        self.black = np.zeros(self.frame.shape[:2], np.uint8)
        self.kernel = np.ones((21, 21), np.uint8)
        self.mask = cv2.erode(self.mask, self.kernel)

    # contours function
    def contours_detect(self):
        self.masking()
        self.contours, self.no_use = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(self.contours) != 0:
            for contour in self.contours:
                if cv2.contourArea(contour) > 2500:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(self.frame, [box], -1, (255, 0, 0), 3)
                    (self.x, self.y), (self.w, self.h), self.angle = rect
        rectangle = cv2.rectangle(self.black.copy(), (int(self.x - self.var), int(self.y - self.var)),
                                  (int(self.x + self.var), int(self.y + self.var)), 255, -1)
        self.masking_ball = cv2.bitwise_and(self.frame, self.frame, mask=rectangle)

    # show frame function
    def show(self):
        self.contours_detect()
        self.arduino.write(str.encode(f"{self.x},{self.y}"))
        cv2.imshow("Main", self.frame)
        cv2.imshow("vid", self.mask)
        cv2.imshow("vid_original", self.masking_ball)
