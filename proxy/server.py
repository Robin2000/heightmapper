#!/usr/bin/env python3
# coding=utf-8

import simple_http_server.server as server
# 如果你的控制器代码（处理请求的函数）放在别的文件中，那么在你的 main.py 中，你必须将他都 import 进来。
import google
import nextzen
import thunderforest


def main(*args):
    # 除了 import 外，还可以通过 scan 方法批量加载 controller 文件。
    #server.scan("my_ctr_pkg", r".*controller.*")
    #server.start(host="127.0.0.1", port=8080)
    server.start(host="127.0.0.1", port=8080, resources={"D:/heightmapper/robin2000/heightmapper/*"})
    """
        server.start(host="127.0.0.1", 
                 port=8443,
                 ssl=True,
                 ssl_protocol=ssl.PROTOCOL_TLS_SERVER, # 可选，默认使用 ssl.PROTOCOL_TLS_SERVER，该配置会使得服务器取客户端和服务端均支持的最高版本的协议来进行通讯。
                 ssl_check_hostname=False, # 可选，是否检查域名，如果设为 True，那么如果不是通过该域名访问则无法建立对应链接。
                 keyfile="/path/to/your/keyfile.key",
                 certfile="/path/to/your/certfile.cert",
                 keypass="", # 可选，如果你的私钥使用了密码加密
                 )
    """
if __name__ == "__main__":
    main()
