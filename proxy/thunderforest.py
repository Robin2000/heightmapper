from simple_http_server import request_map
from simple_http_server import Response
from simple_http_server import PathValue
import os
from urllib.request import urlopen,Request
import ssl


def read_url(file,header,IMAGE_URL):
   if os.path.exists(file):
       with open(file, 'rb') as f:
           content=f.read()
           f.close()
           return content

   request = Request(IMAGE_URL, headers=header)
   contex = ssl._create_unverified_context()
   pic_data_url = urlopen(request,context=contex)
   pic_data = pic_data_url.read()

   with open(file, 'wb') as f:
        f.write(pic_data)
        f.close()
   return pic_data


@request_map("/thunderforest/{x}/{y}/{z}", method="GET")
def thunderforest_ctroller_function(x=PathValue("x"),y=PathValue("y"),z=PathValue("z"),res=Response()):
    file = '/cache/thunderforest/'+x+"_"+y+"_"+z+".png"
    headers={}
    headers['referer']='http://www.topwow.top:8000/' 
    headers['accept']='image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    headers['origin']='http://www.topwow.top:8000'
    headers['sec-fetch-dest']='image'
    headers['sec-fetch-mode']='cors'
    headers['sec-fetch-site']='cross-site'
    headers['User-Agent']= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50'
    content = read_url(file, headers, "https://tile.thunderforest.com/cycle/"+z+"/"+x+"/"+y+".png?apikey=3e8dd0f399bd45a290a515026bb63a2a")
    res.headers["Content-Type"] = "image/png"
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.body = content
    res.send_response()


    