import cv2
from pypylon import pylon
import json
from datetime import datetime

detector = cv2.QRCodeDetector()

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

camera.AcquisitionFrameRateEnable.Value = True
camera.AcquisitionFrameRate.Value = 60.0
camera.ExposureTime.Value = 1300.0

camera.MaxNumBuffer = 10

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

window_name = 'QR Code Detection'

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data from the Basler camera
        image = converter.Convert(grabResult)
        img = image.GetArray()

        # QR code detection
        ret_qr, decoded_data, points, _ = detector.detectAndDecodeMulti(img)
        if ret_qr:
            # If QR codes are detected, draw the bounding box and display the decoded text
            for s, p in zip(decoded_data, points):
                if s:
                    print(f"QR Code detected: {s}")
                    # Save the time and frame number into a JSON file
                    data = {'time': datetime.now().isoformat(), 'frame_number': s}
                    with open('qr_scans.json', 'a') as f:
                        f.write(json.dumps(data) + '\n')
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                img = cv2.polylines(img, [p.astype(int)], True, color, 8)

        # Show the image with detected QR codes
        cv2.imshow(window_name, img)

        if cv2.waitKey(1) == ord('q'):
            break

    grabResult.Release()

camera.StopGrabbing()
cv2.destroyAllWindows()

differences = []

with open('qr_scans.json', 'r') as f:
    lines = f.readlines()

    for line in lines:
        record = json.loads(line)
        time_left_str = record['time']
        frame_info = record['frame_number']

        time_right_str = frame_info.split('QR Code: ')[1].split(' - Frame:')[0]

        time_left = datetime.strptime(time_left_str, '%Y-%m-%dT%H:%M:%S.%f')
        time_right = datetime.strptime(time_right_str, '%Y-%m-%d %H:%M:%S.%f')

        diff = (time_left - time_right).total_seconds() * 1000

        differences.append(diff)

    mean_difference = sum(differences) / len(differences)
    print(f"The mean difference is approximately {mean_difference:.3f} milliseconds.")