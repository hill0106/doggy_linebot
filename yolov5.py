import cv2
import numpy as np
import torch
from azure_blob import *

#使用自己訓練的model best.pt來計算
model = torch.hub.load('ultralytics/yolov5', 'custom', path='exp14/weights/best.pt', force_reload=True)
def detect(path):
    #設定多少confidence以上才可以顯示出來
    if model.conf >= 0.2:
        img = cv2.imread(path)
        results = model(img)
        if len(results.xyxy[0].tolist()) == 0:
            return False
        else:
           
            tensor = results.xyxy[0]
            cv2.imwrite('static/result.jpeg',np.squeeze(results.render()))
            return str(int(tensor.tolist()[0][5]))
    else:
        return False
