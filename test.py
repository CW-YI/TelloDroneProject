import cv2
from djitellopy.tello import Tello

tello=Tello()
tello.connect()
print(f'battery remaining amount :{tello.get_battery()}')

tello.streamon()
while True:
    img=tello.get_frame_read().frame
    img=cv2.resize(img, (720, 480))
    cv2.imshow("Image", img)
    cv2.waitKey(1)