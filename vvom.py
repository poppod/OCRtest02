from camera_detect import WebcamVideoStream
import cv2
camera=WebcamVideoStream(src=1).start()

while True:
    (frame) = camera.read()
    # image = frame



    # image_center = (image.shape[0] / 2, image.shape[1] / 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    # cv2.cv2.drawContours()
camera.release()
cv2.destroyAllWindows()