#!/usr/bin/python
# -*- coding:utf-8 -*-

#import time
#from PIL import Image,ImageDraw,ImageFont, ImageEnhance
#import cv2
#import numpy as np
#import PIL
#import sys
#from eink_python3 import epd7in5, epdconfig
import os, random
from redis import Redis
from rq import Queue
from tasks import convert_and_show

## Redis queue
q = Queue(connection=Redis())

def main():

    folder = '/home/pi/Desktop/Ivalo_2020/'
    ### get random file from escape folder
    filename = random.choice(os.listdir(folder))
    #print(filename)
    filepath = os.path.join(folder, filename)
    #print(filepath)
    tasks = q.enqueue(convert_and_show, filepath,result_ttl=0)

    

if __name__ == "__main__":
    main()
    

