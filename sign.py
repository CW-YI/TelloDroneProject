import sys
import numpy as np
import cv2
from djitellopy.tello import Tello
import tensorflow.keras
import algorithm as al

tello = Tello()
tello.connect()
print(f'battery remainig amount : {tello.get_battery()}')
tello.streamon() # 비디오 화면 전송 시작
model_file = 'C:/Users/asm96/Documents/python/tello_drone/converted_keras/keras_model.h5'
model = tensorflow.keras.models.load_model(model_file)

path = { # 딕셔너리 immutable한 키와 mutable한 값으로 맵핑되어있는 순서가 없는 집합 → 인덱스로 접근할 수 없음
    'A': {'BC': 46, 'BE': 69, 'CE': 69}, # 키 / 값
    'B': {'AC': 63, 'AD': 156, 'AE': 120, 'CD': 93, 'CE': 173, 'DE': 80},
    'C': {'AB': 69, 'AD': 115, 'BD': 46},
    'D': {'BC': 58, 'BF': 96, 'CF': 154},
    'E': {'AB': 31, 'AF': 124, 'BF': 93},
    'F': {'ED': 91}
}

def preprocessing(frame):
    size = (224, 224)
    frame_resize = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    frame_normalize = (frame_resize.astype(np.float32) / 127.0) - 1
    frame_reshape = frame_normalize.reshape((1, 224, 224, 3))
    return frame_reshape

def predict(frame):
    prediction = model.predict(frame)
    return prediction


start = input('출발점을 입력하세요 : ')
end = input('도착점을 입력하세요 : ')
course = al.path(start, end)

while True:
    turn = 0
    img = tello.get_frame_read().frame

    preprocess = preprocessing(img)
    prediction = predict(preprocess)

    #0.none 1.up 2.down 3.turn
    max = 0
    for x in range(4):
        if prediction[0,x] > max:
            max = prediction[0,x]

    if prediction[0,0] == max:
        pass # none

    elif prediction[0,1] == max: # up
        print(f'battery remaining : {tello.get_battery()}')
        tello.takeoff() # 이륙

    elif prediction[0,2] == max: # down
        print(f'battery remaining : {tello.get_battery()}')
        tello.land() # 착륙

    elif prediction[0,3] == max: # turn
        print(f'battery remaining : {tello.get_battery()}')
        course[turn+1]
        for node, angle in path[course[turn+1]].items():
            if course[turn] + course[turn+2] == node:
                tello.cw(angle)
        turn+=1


    #img = cv2.resize(img, (360, 240)) # 화면 크기
    cv2.imshow("Image", img) # 화면을 표시할 창의 이름, 화면
    #cv2.waitKey(1) # 키보드 입력을 기다림

