import PID_Project
import cv2

pid = PID_Project.Ball()
pid.Trackbar()

while True:
    pid.trackbar_elements()
    pid.Frame_detect()
    pid.masking()
    pid.contours_detect()
    pid.show()
    key = cv2.waitKey(1)
    if key & 0xFF == ord(' '):
        break

pid.get_vid().release()
cv2.destroyAllWindows()
