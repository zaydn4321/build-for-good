import cv2  # 1
import time  # 2

cap = cv2.VideoCapture(0)  # 3

try:  # 4
    while True:  # 5
        ret, frame = cap.read()  # 6

        if ret:  # 7
            cv2.imshow('Frame', frame)  # 8

            current_time = int(time.time())  # 9
            if current_time % 5 == 0:  # 10
                cv2.imwrite('frame-{}.jpg'.format(current_time), frame)  # 11

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 12
                break  # 13
        else:  # 14
            break  # 15
finally:  # 16
    cap.release()  # 17
    cv2.destroyAllWindows()  # 18
