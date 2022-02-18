import cv2


def webcam_snap():
    camera = cv2.VideoCapture(0)
    while True:
        return_value, image = camera.read()
        if cv2.waitKey(1):
            cv2.imwrite("webcam.jpg", image)
            break
    camera.release()
    cv2.destroyAllWindows()
