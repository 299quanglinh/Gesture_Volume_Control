import cv2
import time 
import numpy as np
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities

###############################
wCam, hCam = 1280, 720
###############################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

# Cấu hình thiết bị âm thanh qua Pycaw
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

# Lấy dải âm lượng của hệ thống (dB)
volRange = volume.GetVolumeRange()
minVol = volRange[0]   # Mức âm lượng nhỏ nhất (thường là -65.25 dB)
maxVol = volRange[1]   # Mức âm lượng lớn nhất (0.0 dB)

# Khởi tạo các giá trị ban đầu cho thanh Volume Bar
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Lật gương hình ảnh để cử chỉ tự nhiên

    # 1. Phát hiện bàn tay và lấy vị trí các điểm mốc
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tọa độ ngón cái (mốc 4) và ngón trỏ (mốc 8)
        x1, y1 = lmList[4][1:]
        x2, y2 = lmList[8][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Điểm trung tâm giữa 2 đầu ngón

        # Vẽ điểm mốc và đường nối màu Neon Cyan (255, 255, 0)
        cv2.circle(img, (x1, y1), 10, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
        cv2.circle(img, (cx, cy), 8, (255, 255, 0), cv2.FILLED)

        # Tính khoảng cách giữa 2 đầu ngón tay
        length = math.hypot(x2 - x1, y2 - y1)

        # 2. Quy đổi khoảng cách tay (50 -> 220 px) sang:
        # - Mức âm lượng dB: minVol -> maxVol
        # - Chiều cao thanh Bar hiển thị: 400 -> 150 px
        # - Phần trăm âm lượng: 0% -> 100%
        vol = np.interp(length, [50, 220], [minVol, maxVol])
        volBar = np.interp(length, [50, 220], [400, 150])
        volPer = np.interp(length, [50, 220], [0, 100])

        # Áp dụng thay đổi âm lượng vào hệ thống máy tính
        volume.SetMasterVolumeLevel(vol, None)

        # Đổi điểm trung tâm sang màu đỏ khi 2 ngón tay chạm sát nhau (< 50)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

    # 3. Vẽ thanh hiển thị âm lượng (Volume Bar)
    # Khung viền thanh volume
    cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 0), 2)
    # Phần ruột hiển thị mức âm lượng hiện tại
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 255, 0), cv2.FILLED)
    # Hiển thị số phần trăm (%)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 1)

    # 4. Tính toán và hiển thị FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 0), 1)

    # Hiển thị cửa sổ
    cv2.imshow("Volume Hand Control", img)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()