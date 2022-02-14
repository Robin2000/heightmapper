#!/usr/bin/env python3
# coding=utf-8

import socket
from threading import Thread


class Proxy:
    def __init__(self, port=3000):
        self.port = port
        self.proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = 4096

    def run(self):
        self.proxy.bind(("0.0.0.0", self.port))
        self.proxy.listen(100)
        print("  * Proxy server is running on port {}".format(self.port))

        while True:
            client, addr = self.proxy.accept()
            print(" => {}:{}".format(addr[0], addr[1]))
            Thread(target=self.handle_request, args=(client,)).start()

    def handle_request(self, client):
        head = self.parse_head(client.recv(self.buffer_size))
        headers = head["headers"]
        request = "{}\r\n".format(head["meta"])
        for key, value in headers.items():
            request += "{}: {}\r\n".format(key, value)
        request += "\r\n"
        if "content-length" in headers:
            while len(head["chunk"]) < int(headers["content-length"]):
                head["chunk"] += client.recv(self.buffer_size)

        request = request.encode() + head["chunk"]
        port = 80
        try:
            tmp = head["meta"].split(" ")[1].split("://")[1].split("/")[0]
        except IndexError:
            client.close()
            return
        if tmp.find(":") > -1:
            port = int(tmp.split(":")[1])

        response = self.send_to_server(headers["host"], port, request)
        client.sendall(response)
        client.close()


    def send_to_server(self, host, port, data):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((socket.gethostbyname(host), port))
        server.sendall(data)

        head = self.parse_head(server.recv(4096))
        headers = head["headers"]
        response = "{}\r\n".format(head["meta"])
        for key, value in headers.items():
            response += "{}: {}\r\n".format(key, value)
        response += "\r\n"

        if "content-length" in headers:
            while len(head["chunk"]) < int(headers["content-length"]):
                head["chunk"] += server.recv(self.buffer_size)

        response = response.encode() + head["chunk"]
        server.close()
        return response


    def parse_head(self, head_request):
        nodes = head_request.split(b"\r\n\r\n")
        heads = nodes[0].split(b"\r\n")
        meta = heads.pop(0).decode("utf-8")
        data = {
            "meta": meta,
            "headers": {},
            "chunk": b""
        }

        if len(nodes) >= 2:
            data["chunk"] = nodes[1]

        for head in heads:
            pieces = head.split(b": ")
            key = pieces.pop(0).decode("utf-8")
            if key.startswith("Connection: "):
                data["headers"][key.lower()] = "close"
            else:
                data["headers"][key.lower()] = b": ".join(pieces).decode("utf-8")
        return data


if __name__ == "__main__":
    proxy = Proxy(3001)
    proxy.run()