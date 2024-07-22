import tensorflow.keras
import numpy as np
import cv2
from djitellopy.tello import Tello
import algorithm as al

# 모델 위치
model_filename ='C:\\Users\\asm96\\Documents\\python\\tello_drone\\keras_model.h5'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

tello=Tello()
tello.connect()
tello.streamon()

# 카메라를 제어할 수 있는 객체
capture = tello.get_frame_read().frame


# 이미지 처리하기
def preprocessing(frame):

    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    #print(frame_reshaped)
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

path = { # 딕셔너리 immutable한 키와 mutable한 값으로 맵핑되어있는 순서가 없는 집합 → 인덱스로 접근할 수 없음
    'A': {'BC': 46, 'BE': 69, 'CE': 69}, # 키 / 값
    'B': {'AC': 63, 'AD': 156, 'AE': 120, 'CD': 93, 'CE': 173, 'DE': 80},
    'C': {'AB': 69, 'AD': 115, 'BD': 46},
    'D': {'BC': 58, 'BF': 96, 'CF': 154},
    'E': {'AB': 31, 'AF': 124, 'BF': 93},
    'F': {'ED': 91}
}

start = input('출발점을 입력하세요 : ')
end = input('도착점을 입력하세요 : ')
course = al.path(start, end)

while True:
    max = 0
    turn = 0
    
    frame = tello.get_frame_read().frame

    if cv2.waitKey(100) > 0: 
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)

    for x in range(4):
        if prediction[0,x] > max:
            max = prediction[0,x]

    if (prediction[0,1] == max) and (tello.is_flying == 0):
        print('up')
        cv2.putText(frame, 'up', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print(f'battery remaining : {tello.get_battery()}')
        tello.takeoff() # 이륙
        #tello.get_height() == 30

    elif (prediction[0,2] == max) and (tello.is_flying == 1):
        print('down')
        cv2.putText(frame, 'down', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print(f'battery remaining : {tello.get_battery()}')
        tello.land() # 착륙
        tello.streamoff
        break

    elif (prediction[0,3] == max) and (tello.is_flying == 1) and (len(course)-2 > turn):
        print('turn')
        cv2.putText(frame, 'turn', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print(f'battery remaining : {tello.get_battery()}')
        for node, angle in path[course[turn+1]].items():
            if course[turn] + course[turn+2] == node:
                print(180-angle)
                tello.rotate_clockwise(180-angle)
        turn+=1

    else:
        cv2.putText(frame, 'none', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print('none')

    tello.send_rc_control(0,15,0,0)


    cv2.imshow("VideoFrame", frame)