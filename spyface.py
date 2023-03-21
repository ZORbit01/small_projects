import cv2
import time
import requests
from datetime import datetime
import re
import os
from threading import Thread

path = '/photo/path/here'
def send_hook():
    try:
        mUrl = "https://discord.com/api/webhooks/yourdiscordwebhook"
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        data = {"content": 'new Linux login attempt at '+dt_string}
        response = requests.post(mUrl, json=data)
    except :
        pass

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    if(len(paths) == 0) :
        return 0
    return max(paths, key=os.path.getctime)


def calculate_image_nb():
    elnew = newest(path)
    if(elnew == 0 ):
        return 0
    else:
        extnb = int(re.search(r'\d+', elnew).group())
        return extnb

def capture():
    camera = cv2.VideoCapture(0)
    extnb = calculate_image_nb()
    for i in range(extnb,extnb + 5):
        return_value, image = camera.read()
        cv2.imwrite(path+str(i)+'.png', image)
        time.sleep(5)
    del(camera)

if __name__ == '__main__':
    Thread(target = capture).start()
    Thread(target = send_hook).start()
