import cv2
from pypylon import pylon

detector = cv2.QRCodeDetector()

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

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
