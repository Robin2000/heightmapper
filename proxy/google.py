#!/usr/bin/env python3
# coding=utf-8

from simple_http_server import request_map
from simple_http_server import Response
from simple_http_server import PathValue
from urllib.parse import urlencode
import os,math
from io import BytesIO
from PIL import Image,ImageChops

def read_url(fileName,IMAGE_URL):
   file = '/cache/google/'+fileName
   if os.path.exists(file):
       with open(file, 'rb') as f:
           content=f.read()
           f.close()
           return content
   import requests
   r = requests.get(IMAGE_URL)
   with open(file, 'wb') as f:
        f.write(r.content)
        f.close()
   return r.content

def ImgOfffSet(Img,xoff,yoff):
    width, height = Img.size
    c = ImageChops.offset(Img,xoff,yoff)
    c.paste((0,0,0),(0,0,xoff,height))
    c.paste((0,0,0),(0,0,width,yoff))
    return c

@request_map("/google/{x}/{y}/{z}", method="GET")
def google_ctroller_function(x=PathValue("x"),y=PathValue("y"),z=PathValue("z"),res=Response()):
    x,y,z=int(x),int(y),int(z)
    zp=math.pow(2,z)
    
    if z==15:
        offsetX,offsetY=51,78
    elif z==16:
        offsetX,offsetY=98,149
    elif z==17:
        offsetX,offsetY=196,300
    elif z==18:
        offsetX,offsetY=396,597
    else:
        offsetX,offsetY=int(0.001556396*zp),int(0.002380371*zp) 

    M,N=math.ceil(offsetX/256)+1,math.ceil(offsetY/256)+1
    imgArr=[]
    for i in range(M):
       row=[]
       for j in range(N):
          r,c=str(x+i),str(y+j)
          content=read_url(r+"_"+c+"_"+str(z)+".png", "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x="+r+"&y="+c+"&z="+str(z))
          imgByte=BytesIO(content)
          img=Image.open(imgByte)
          row.append(img)
          #imgByte.close()
       imgArr.append(row)
    
    w,h=imgArr[0][0].size;
    newimg = Image.new(mode="RGB", size=(w*M,h*N))
    for i in range(M):
       for j in range(N):
          newimg.paste(imgArr[i][j],(i*w,j*h))

    newimg=ImgOfffSet(newimg,-offsetX, -offsetY) 

    box = (0, 0, w, h)
    newimg=newimg.crop(box)

    imgByte=BytesIO()
    newimg.save(imgByte, format='PNG')
    content=imgByte.getvalue()
    #imgByte.close()

    res.headers["Content-Type"] = "image/png"
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.body = content
    res.send_response()

@request_map("/google01/{x}/{y}/{z}", method="GET")
def google_ctroller_function01(x=PathValue("x"),y=PathValue("y"),z=PathValue("z"),res=Response()):
    y2=str(int(y)+1)
    google_ctroller_function(x,y2,z,res)

@request_map("/google10/{x}/{y}/{z}", method="GET")
def google_ctroller_function10(x=PathValue("x"),y=PathValue("y"),z=PathValue("z"),res=Response()):
    x2=str(int(x)+1)
    google_ctroller_function(x2,y,z,res)

@request_map("/google11/{x}/{y}/{z}", method="GET")
def google_ctroller_function11(x=PathValue("x"),y=PathValue("y"),z=PathValue("z"),res=Response()):
    y2=str(int(y)+1)
    x2=str(int(x)+1)
    google_ctroller_function(x2,y2,z,res)
