import PID_Project
import cv2

pid = PID_Project.Ball()


while True:
    pid.show()
    key = cv2.waitKey(1)
    if key & 0xFF == ord(' '):
        break

pid.get_vid().release()
cv2.destroyAllWindows()
