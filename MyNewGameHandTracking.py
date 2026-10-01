import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()
while True:
    success, img = cap.read()
    if not success:
        continue
    img = cv2.flip(img, 1)  # Lật gương
    img = cv2.resize(img, (0, 0), fx=2, fy=2)  # Tăng kích thước webcam x2
    img = detector.findHands(img)
    lmdList = detector.findPosition(img)
    if len(lmdList) != 0:
        print(lmdList[4])
    cTime = time.time() 
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)