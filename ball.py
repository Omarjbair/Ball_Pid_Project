import cv2
import numpy as np
import serial

def nothing1(x):
    pass

vid = cv2.VideoCapture(0)

x, y, w, h, angle = 0,0,0,0,0
saturation,Value = 0,0
sum, count, sum_2, count_2 = 0,0,0,0
var = 100
trakbar_name = "trakpar_ball"
cv2.namedWindow(trakbar_name )
cv2.createTrackbar("exposure",trakbar_name ,1,7,nothing1)
cv2.createTrackbar("min_h",trakbar_name ,0,180,nothing1)
cv2.createTrackbar("max_h",trakbar_name ,0,180,nothing1)

while True:
    exposure = cv2.getTrackbarPos("exposure",trakbar_name )
    min_h = cv2.getTrackbarPos("min_h",trakbar_name )
    max_h = cv2.getTrackbarPos("max_h",trakbar_name )
    lower = np.array([min_h,saturation,Value])
    upper = np.array([max_h,255,255])
    vid.set(15,-exposure)
    nothing, frame = vid.read()
    frame = cv2.GaussianBlur(frame,(7,7),0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            sum_2 += hsv[i,j][2]
            count_2 += 1
            sum += hsv[i,j][1]
            count += 1
    Value = sum_2 // count_2
    saturation = sum // count
    mask = cv2.inRange(hsv, lower, upper)
    black = np.zeros(frame.shape[:2], np.uint8)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.erode(mask,kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 1500:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], -1, (255, 0, 0), 3)
                (x, y), (w, h), angle = rect 
    rectangle = cv2.rectangle(black.copy(), (int(x - var), int(y - var)), (int(x + var), int(y + var)), 255, -1)
    masking_ball = cv2.bitwise_and(frame, frame, mask=rectangle)
    cv2.imshow("vid", cv2.flip(mask, 1))
    cv2.imshow("vid_original", cv2.flip(masking_ball, 1))
    key = cv2.waitKey(1)
    if key & 0xFF == ord(' '):
        break

vid.release()
cv2.destroyAllWindows()