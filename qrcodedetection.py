import cv2
import time

camera_id = 1
window_name = 'QR Code Detection'

detector = cv2.QRCodeDetector()
cap = cv2.VideoCapture(camera_id)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        ret_qr, decoded_data, points, _ = detector.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_data, points):
                if s:
                    print(s)
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
        cv2.imshow(window_name, frame)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyWindow(window_name)