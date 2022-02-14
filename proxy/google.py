from simple_http_server import request_map
from simple_http_server import Response
from simple_http_server import PathValue
from urllib.parse import urlencode
import os


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


@request_map("/google/{x}/{y}/{z}", method="GET")
def google_ctroller_function(x=PathValue("x"),y=PathValue("y"),z=PathValue("z"),res=Response()):
    content = read_url(x+"_"+y+"_"+z+".png", "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x=" + x+ "&y=" +y+ "&z=" + z)
    res.headers["Content-Type"] = "image/png"
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.body = content
    res.send_response()
