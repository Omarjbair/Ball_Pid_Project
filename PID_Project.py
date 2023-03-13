# import library
import cv2
import numpy as np


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
        self.sum = 0
        self.count = 0
        self.sum2 = 0
        self.count2 = 0
        self.stop = 0
        self.var = 100
        self.trackbar_name = "trackpar_ball"
        self.vid = cv2.VideoCapture(0)

    # Do_nothing function
    def nothing(self):
        pass

    #get vid
    def get_vid(self):
        return self.vid

    # Trackbar function
    def Trackbar(self):
        cv2.namedWindow(self.trackbar_name)
        cv2.createTrackbar("exposure", self.trackbar_name, 1, 7, self.nothing)
        cv2.createTrackbar("min_h", self.trackbar_name, 0, 180, self.nothing)
        cv2.createTrackbar("max_h", self.trackbar_name, 0, 180, self.nothing)

    def trackbar_elements(self):
        self.exposure = cv2.getTrackbarPos("exposure", self.trackbar_name)
        self.min_h = cv2.getTrackbarPos("min_h", self.trackbar_name)
        self.max_h = cv2.getTrackbarPos("max_h", self.trackbar_name)
        self.lower = np.array([self.min_h, self.saturation, self.value])
        self.upper = np.array([self.max_h, 255, 255])
        self.vid.set(15, -self.exposure)

    # frame function
    def Frame_detect(self):
        self.trackbar_elements()
        self._, self.frame = self.vid.read()
        self.frame = cv2.GaussianBlur(self.frame, (7, 7), 0)
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        for i in range(self.frame.shape[0]):
            for j in range(self.frame.shape[1]):
                self.sum_2 += self.hsv[i, j][2]
                self.count_2 += 1
                self.sum += self.hsv[i, j][1]
                self.count += 1
        self.value = self.sum_2 // self.count_2
        self.saturation = self.sum // self.count

    # masking function
    def masking(self):
        self.Frame_detect()
        self.mask = cv2.inRange(self.hsv, self.lower, self.upper)
        self.black = np.zeros(self.frame.shape[:2], np.uint8)
        self.kernel = np.ones((3, 3), np.uint8)
        self.mask = cv2.erode(self.mask, self.kernel)

    # contours function
    def contours_detect(self):
        self.masking()
        self.contours, self.no_use = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(self.contours) != 0:
            for contour in self.contours:
                if cv2.contourArea(contour) > 1500:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(self.frame, [box], -1, (255, 0, 0), 3)
                    (self.x, self.y), (self.w, self.h), self.angle = rect
        rectangle = cv2.rectangle(self.black.copy(), (int(self.x - self.var), int(self.y - self.var)), (int(self.x + self.var), int(self.y + self.var)), 255, -1)
        self.masking_ball = cv2.bitwise_and(self.frame, self.frame, mask=rectangle)

    # show frame function
    def show(self):
        self.contours_detect()
        cv2.imshow("vid", cv2.flip(self.mask, 1))
        cv2.imshow("vid_original", cv2.flip(self.masking_ball, 1))
