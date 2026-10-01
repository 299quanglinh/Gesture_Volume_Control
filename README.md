# Gesture Volume Control 👋🔊

Điều khiển âm lượng máy tính bằng cử chỉ bàn tay thông qua Webcam, sử dụng **OpenCV**, **MediaPipe** và **Pycaw**.

## 🌟 Tính năng
- Nhận diện bàn tay chính xác theo thời gian thực (21 điểm mốc).
- Đo khoảng cách giữa đầu ngón cái và ngón trỏ để điều chỉnh âm lượng máy tính (0% - 100%).
- Giao diện trực quan phong cách Neon Cyan:
  - Cột Volume Bar hiển thị mức âm lượng theo thời gian thực.
  - Hiệu ứng đổi màu cảnh báo (màu đỏ khi ngón tay chụm lại < 50px).
  - Hiển thị chỉ số FPS.

## 🛠️ Cài đặt

1. Kích hoạt môi trường ảo:
```bash
source .venv/Scripts/activate   # Trên Git Bash
# hoặc
.\.venv\Scripts\Activate.ps1    # Trên PowerShell
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install opencv-python mediapipe pycaw numpy
```

## 🚀 Cách chạy chương trình
```bash
python VolumeHandControl.py
```
- Đưa tay trước camera:
  - Mở rộng khoảng cách ngón cái và ngón trỏ để tăng âm lượng.
  - Chụm 2 ngón tay lại để giảm âm lượng.
- Nhấn phím `q` để thoát chương trình.
