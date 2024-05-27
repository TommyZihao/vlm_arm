# utils_camera.py
# 同济子豪兄 2024-5-22
# 开启摄像头，调用摄像头实时画面，按q键退出

import cv2
import numpy as np

def check_camera():
    '''
    开启摄像头，调用摄像头实时画面，按q键退出
    '''
    print('开启摄像头')
    cap = cv2.VideoCapture(0)
    
    while(True):
        ret, frame = cap.read()
    
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()