#!/usr/bin/python
# -*- coding:utf-8 -*-

#import time
from PIL import Image, ImageEnhance, ImageFilter,ImageDraw,ImageFont
import PIL
#npimport sys
import cv2
from eink_python3 import epd7in5, epdconfig
#import os, random

def eink_img(img):
    print('displaying')
    epd = epd7in5.EPD();
    epd.init();
    epd.display(epd.getbuffer(img));
  

def convert_and_show(filepath):

    #prepare image
    # resize image
    # (640,384) for 7.5 inch
    # (263,176) for 2.7
    # (212,104) for 2.13 
    #size = (640,384)
    print(filepath)
    img = check_size(filepath)
    #print('checked size')
    img_bw = img.convert('1')
    #print('converted')
    #epd = epd7in5.EPD();
    #epd.init();
    #epd.Clear(0xFF)
    #display the image
    eink_img(img_bw)
    print('done')

    
def check_size(f, im = False):
    if im ==False:
        im = Image.open(f)
    else:
        cv2_im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
        im = Image.fromarray(cv2_im)
    
    enhancer = ImageEnhance.Brightness(im)
    enhanced_im = enhancer.enhance(1.8)
    im = enhanced_im
    
    w,h = im.size # h, w, channel
    if im.size ==(640,384):
        return(im)
    #print(size)
    ratio = 640/384 # 1.667
    
    #optionally flip image
    #if size[0] > size[1]:
    #    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) 
    
    ratio_img = w/h
    range_min = 1.5
    range_max = 1.8
    
    # check if in range
    if range_min <= ratio_img <= range_max:
        return(img.resize((640,384),PIL.Image.LANCZOS))
    
    else:
        # width remains the same
        if w>h:
            new_w = 640
            new_h = int(h*640/w)
            #size = (new_w,new_h)
            #old_im = im.resize(size,PIL.Image.LANCZOS)
        elif h>w:
            new_h = 384
            new_w = int(w*384/h)
        size = (new_w,new_h)
        old_im = im.resize(size,PIL.Image.LANCZOS)
        
        new_im = Image.new("RGB", (640,384))
        new_im.paste(old_im, (int((640-size[0])/2),
                      int((384-size[1])/2)))

        return(new_im)
    
def brighten(img, ratio = 1.3):
    enhancer = ImageEnhance.Brightness(img)
    enhanced_im = enhancer.enhance(ratio)
    return(enhanced_im)


  
def slow_video_image(video_name, frame):
    
    vidcap = cv2.VideoCapture(video_name)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    ### convert video to jpg
    fname = '/home/pi/eink/frame.txt'
    frame=0
    with open(fname,'r') as f:
        frame = int(f.read())
        
    vidcap = cv2.VideoCapture(video_name)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    #print('Number of frames {}'.format(length))
    #print('Adjusting lighting by {}'.format(light))
    size = (640,384)
    # (640,384) for 7.5 inch
    # (263,176) for 2.7
    # (212,104) for 2.13
    
    
    if frame > length:
        frame = 0
        
    vidcap.set(1,frame)
    success,img = vidcap.read()    
    
    img = check_size(filepath, img)

    img_bw = img.convert('1')

    #epd = epd7in5.EPD();
    #epd.init();
    #epd.Clear(0xFF)
    #display the image
    eink_img(img_bw)
    
    inc = 10 #random.randint(30,90)
    frame += inc


    with open(fname,'w') as f:
        f.write(str(frame))

#f __name__ == "__main__":
#    main()
    


