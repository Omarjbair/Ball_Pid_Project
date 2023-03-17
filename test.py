from ctypes.wintypes import POINT
from email.mime import image
from turtle import clone, color
import cv2
import numpy as np

window_name = "image"
crop_window_name = "croped-image"
cv2.namedWindow(window_name)

img = cv2.imread("img1.jpg")

point = []
clone = img.copy()

def mouse_callback(event, x, y, flags, param):

    global clone

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.destroyAllWindows(crop_window_name)
        clone = img.copy()
        point.append(x,y)
    if cv2.EVENT_LBUTTONUP:
        point.append(x,y)



colors = {'red' : (0,0,255) , 'green' : (0,255,0)}
cv2.setMouseCallback(window_name,mouse_callback,param = colors)
while True:
    cv2.imshow(window_name,clone)
    if cv2.waitKey(22) & 0xFF == ord('q'):
        break
cv2.waitKey(0)