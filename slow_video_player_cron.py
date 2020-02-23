#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
#from eink_python3 import epd7in5, epdconfig
import os, random
from redis import Redis
from rq import Queue
from tasks import convert_and_show

## Redis queue
q = Queue(connection=Redis())

video_name = '/home/pi/eink/Avengers.Infinity.War.2018.mkv'
framefile = '/home/pi/eink/frame.txt'


def main():

    taks = q.enqueue(slow_video_image, video_name, framefile,
                     result_ttl=0)
    
    

if __name__ == "__main__":
    main()
    

