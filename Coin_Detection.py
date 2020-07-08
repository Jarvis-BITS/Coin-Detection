import cv2
import numpy as np
import math

# Func to cal eucledian dist b/w 2 pts:


def euc_dst(x1, y1, x2, y2):
    pt_a = (x1 - x2)**2
    pt_b = (y1 - y2)**2
    return math.sqrt(pt_a + pt_b)


cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1,
                               minDist=10, param1=100, param2=50, minRadius=0, maxRadius=500)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        x_cord = []
        y_cord = []
        rad = []
        # Converting parameters of circle (center coordinates:x,y & radius)
        for pt in circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            # Storing centers & radius of all circles
            x_cord.append(x)
            y_cord.append(y)
            rad.append(r)
            # Drawing outer circle
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

            # Drawing circle center
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 3)
        if len(rad) > 1:
            for i in range(0, len(rad)):
                x1 = x_cord[i]
                y1 = y_cord[i]
                for j in range(i+1, len(rad)):
                    x2 = x_cord[j]
                    y2 = y_cord[j]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    mid_x = (x1+x2)/2
                    mid_y = (y1+y2)/2
                    dist = euc_dst(x1/25, y1/25, x2/25, y2/25)
                    cv2.putText(frame, "{:.1f}cm".format(dist), (int(mid_x), int(
                        mid_y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
    cv2.imshow('video', frame)
    if cv2.waitKey(1) == 27:  # esc Key
        break

cap.release()
cv2.destroyAllWindows()
