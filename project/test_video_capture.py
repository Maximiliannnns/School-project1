from itertools import count
import numpy as np
import cv2


cap = cv2.VideoCapture(0)
count1 = 0

while(True): 
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Video', frame)   
    if cv2.waitKey(1) & 0xFF == ord('w'):
        cv2.imwrite(f"photo{count1}.jpg", frame)
        count1+=1
    # cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()