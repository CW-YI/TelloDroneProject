import tensorflow.keras
import numpy as np
import cv2
from djitellopy.tello import Tello

# 모델 위치
model_filename ='C:\\Users\\asm96\\Documents\\python\\tello_drone\\converted_keras\\keras_model.h5'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

tello=Tello()
tello.connect()
tello.streamon()

# 카메라를 제어할 수 있는 객체
#capture = cv2.VideoCapture(tello.streamon) # 0은 내장 카메라
capture = tello.get_frame_read().frame

# 카메라 길이 너비 조절
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#capture=cv2.resize(capture, (320, 240))

# 이미지 처리하기
def preprocessing(frame):
    #frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    # astype : 속성
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    #print(frame_reshaped)
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

while True:
    max = 0
    
    frame = tello.get_frame_read().frame

    if cv2.waitKey(100) > 0: 
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)

    for x in range(4):
        if prediction[0,x] > max:
            max = prediction[0,x]

    if (prediction[0,1] == max):
        print('up')
        cv2.putText(frame, 'up', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

    elif (prediction[0,2] == max):
        print('down')
        cv2.putText(frame, 'down', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

    elif (prediction[0,3] == max):
        print('turn')
        cv2.putText(frame, 'turn', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

    else:
        cv2.putText(frame, 'none', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print('none')

    cv2.imshow("VideoFrame", frame)