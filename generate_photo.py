#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5
import time
import traceback
import cv2
import numpy as np
import time
#import PIL
from random import randint
import numpy

import pylab
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance, ImageFilter,ImageDraw,ImageFont


def brighten(img, ratio = 1.3):
    enhancer = ImageEnhance.Brightness(img)
    enhanced_im = enhancer.enhance(ratio)
    return(enhanced_im)

#take cv2 image capture and return B&W dithered image
def bw_and_resize(img,size1=640,size2=384,cap='',light = 0):
    # (640,384) for 7.5 inch
    # (264,176) for 2.7
    # (212,104) for 2.13 
    size = (size1, size2)
    
    #change brightness
    img_dark = brightness(img.copy(), light + .4)
    img_light = brightness(img.copy(), light - .4)
    img = brightness(img,light)
    
   
    #change from cv2 to PIL for dithering
    p_dark = cv2_to_pil(img_dark)
    p_light = cv2_to_pil(img_light)
    pil_im = cv2_to_pil(img)

    #cartoon and edge images from cv2 to pil
    img_edge = bw_and_edge(img,size1,size2,light)
    img_cartoon= cartoon(img,size1,size2,light) 
    
    #PIL ims resizing
    img = pil_im.resize(size,Image.LANCZOS)
    img_dark = p_dark.resize(size,Image.LANCZOS)
    img_light = p_light.resize(size,Image.LANCZOS)   
    
    #dither images (PIL)
    img_bw = img.convert('1')
    img_dark = img_dark.convert('1')
    img_light = img_light.convert('1')

    #write captions on PIL images
    if cap.strip() != '':
        img_edge = write_text(img_edge,cap.strip())
        img_cartoon= write_text(img_cartoon,cap.strip())
        img_bw = write_text(img_bw,cap.strip())
        img_dark = write_text(img_dark,cap.strip())
        img_light = write_text(img_light,cap.strip())
        
    
    #return PIL images
    return(img_bw, img_cartoon, img_dark, img_light, img_edge)

def text_wrap(s, draw, font, W=640):
    #add a buffer
    W = W-10
    w,h = draw.textsize(s, font)
    print(w,W)
    temp = s.strip()
    s2 = temp.replace('  ', ' ')
    if w >= W:
        # get indices of spaces
        spaces = [i for i,ltr in enumerate(s2) if ltr==' ']
        res = []

        #find last space that fits
        start = 0
        for i in range(len(spaces)):            
            stop = spaces[i]+1
            if draw.textsize(s2[start:stop], font)[0]>=W and i>0:
                res.append(s2[start:stop].strip())
                start = stop
        #print(res)        
        res.append(s2[start:].strip())
        output = '\n'.join(res)

        return(output)
    else:
        return(s2)
    
def write_text(img, rawtext, W=0):
    pointsize = 30
    fillcolor = (255)
    shadowcolor = (0)
    if not W:
        W, H = (640,384)
        
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Roboto-Black.ttf',pointsize)
    text = text_wrap(rawtext,draw, font, W)
    w, h = draw.textsize(text, font=font)

    x,y = ((W-w)/2, (H-h) - 20)

    draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
    draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
    draw.text((x+1, y+1), text, font=font, fill=shadowcolor)

    draw.text((x,y), text, font = font, fill = fillcolor)

    return(img)

    
def cv2_to_pil(img):
    pil_im = Image.fromarray(img)
    return(pil_im)

def cartoon(img,size1,size2,light):
    size = (size1, size2)
    img = cv2.GaussianBlur(img,(5,5),0) 
    img = cv2.resize(img, size)

    a,b = (np.quantile(img, 0.25), np.quantile(img,0.66))
    c = np.quantile(img,0.5)
    #print(a,b)
    
    _,im1 = cv2.threshold(img,a,255,cv2.THRESH_BINARY)
    #_,im2 = cv2.threshold(img,b,255,cv2.THRESH_TOZERO)
    _,im3 = cv2.threshold(img,b,255,cv2.THRESH_BINARY_INV)

    #make the masks
    mask = cv2.bitwise_and(im3, im1)
    imtest = cv2.bitwise_and(img,img,mask=mask)
    white_mask = im3[:,:] == 0
    black_mask = im1[:,:] == 0
    imtest[white_mask] = 255
    imtest[black_mask] = 0
    #imtest[white_mask == black_mask] = c 

    imtest2 = cv2_to_pil(imtest).convert('1')
    
    # calculate countour lines
    v = np.median(imtest)
    sigma = 0.33
    lower = int(max(0, (1.0 - sigma) * v))  
    #upper = int(min(255, (1.0 + sigma) * v))
    edge = cv2.Canny(imtest,  lower, 255)
    #edge = cv2.Canny(imtest,  lower,upper)
    #edge_inv = cv2.bitwise_not(edges)
    
   
    #draw contours
    #_,contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    imtest = cv2.drawContours(np.array(imtest2).astype('uint8'), contours, -1, (0,0,0), 1)
    
    
    #return PIL image
    imtest = Image.fromarray(imtest*255)
    
    return(imtest)

def bw_and_edge(img,size1=640,size2=384,light = 1.0):
    # (640,384) for 7.5 inch
    # (263,176) for 2.7
    # (212,104) for 2.13
    size = (size1, size2)
    gray = cv2.resize(img, size)
    
    img_blur = cv2.GaussianBlur(gray, (3, 3), 0) #cv2.medianBlur(gray, 3)    
    edge = cv2.Canny(gray,  100,255)   
    edge_inv = cv2.bitwise_not(edge)
    
    #return PIL image
    edge_inv = Image.fromarray(edge_inv*1)     
    
    return(edge_inv)

def check_size(im):
    #im = Image.open(f)

    w,h = im.size # h, w, channel
    ratio = 640/384 # 1.667

    ratio_img = w/h
    range_min = 1.5
    range_max = 1.8
    
    # check if in range
    if range_min <= ratio_img <= range_max:
        return(im.resize((640,384),Image.LANCZOS))
    
    else:
        # width remains the same
        if w>h:
            new_w = 640
            new_h = int(h*640/w)

        elif h>w:
            new_h = 384
            new_w = int(w*384/h)
        size = (new_w,new_h)
        old_im = im.resize(size,Image.LANCZOS)

        new_im = Image.new("RGB", (640,384))
        new_im.paste(old_im, (int((640-size[0])/2),
                      int((384-size[1])/2)))

        return(new_im)    

def show_img(filename):
    print('Updating display with ', filename)
    img = Image.open(filename)
    epd = epd7in5.EPD();
    epd.init();
    epd.display(epd.getbuffer(img));
    return()

def clear_epd():
    epd = epd7in5.EPD();
    epd.init();
    epd.Clear(0xFF)
    return()
    
def simple(f):
    print('start')
    size = (640,384)
    im1 = brighten(Image.open(f))
    print('opened')
    im2 = check_size(im1)
    print('checked size')
    im3 = im2.convert('1')
    print('converted')


    epd = epd7in5.EPD();
    epd.init();
    epd.display(epd.getbuffer(im3));
    return()
    #show_img(im3)

def update_img(filename,cap,light=0):
    #read as bw
    im = cv2.imread(filename, 0)
    
    #resize if too big
    size = (640,384)
    temp = im.shape
    if temp[0] > size[0]*3 and temp[1]>size[1]*3:
        im = cv2.resize(im, None, fx=0.5, fy=0.5)
    img = check_size(im)
    
    #light = neg darken or ++ lighten
    img_bw, img_cart, img_dark, img_light, img_edge = bw_and_resize(img,
                                                   size[0],size[1],cap,light)
    temp = randint(0,10000)
    randfilename = str(temp)
    img_bw.save('./static/'+randfilename + 'a.jpg')
    img_cart.save('./static/'+randfilename + 'e.jpg')
    img_edge.save('./static/'+randfilename + 'b.jpg')
    img_dark.save('./static/'+randfilename + 'c.jpg')
    img_light.save('./static/'+randfilename + 'd.jpg')
    
    
    
    return(randfilename)
