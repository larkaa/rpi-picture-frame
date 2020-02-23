#!/usr/bin/python3
# -*- coding:utf-8 -*-

import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


def text_wrap(s, draw, font, W=640):
    #add a buffer
    W = W-10
    #print(s)
    w,h = draw.textsize(s, font)
    #print(w,W)
    #fix text spaces
    temp = s.strip()
    s2 = temp.replace('  ', ' ')
    if w >= W:
        # get indices of spaces
        spaces = [i for i,ltr in enumerate(s2) if ltr==' ']
        res = []
        #print(spaces)

        #find last space that fits
        start = 0
        #print('spaces = ',spaces)
        for i in range(len(spaces)):
            
            stop = spaces[i]+1
            #print(i, stop, s2[stop-1:stop+1])
            if draw.textsize(s2[start:stop], font)[0]>=W and i>0:
                #print(i)
                res.append(s2[start:stop].strip())
                #print(i, ' found : ', s2[start:stop])
                start = stop
                
        res.append(s2[start:].strip())
        output = '\n'.join(res)

        return(output)
    else:
        return(s2)
                
            

pointsize = 30
fillcolor = "white"
shadowcolor = "black"

W, H = (640,384)
rawtext = "You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  You're Pretty.  "
Himage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 255: clear the frame    
draw = ImageDraw.Draw(Himage)
font = ImageFont.truetype('Roboto-Black.ttf',pointsize)
text = edit_text(rawtext,draw, font)
w, h = draw.textsize(text, font=font)
#im = Image.new("RGBA",(W,H),"yellow")
#draw = ImageDraw.Draw(im)

#draw.text(((W-w)/2,(H-h)/2), msg, fill="black")

#640 x 384

epd = epd7in5.EPD()
epd.init()
#print("Clear")
#epd.Clear(0xFF)
#print(w,h)

x,y = ((W-w)/2, (H-h) - 10)

draw.text((x-1, y-1), text, font=font, fill=shadowcolor)
draw.text((x+1, y-1), text, font=font, fill=shadowcolor)
draw.text((x-1, y+1), text, font=font, fill=shadowcolor)
draw.text((x+1, y+1), text, font=font, fill=shadowcolor)

draw.text((x,y), text, font = font, fill = fillcolor)
#print(text)



epd.display(epd.getbuffer(Himage))

