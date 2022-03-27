from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from scrap_engine import Box

class Client():
    player:Box
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        addr = "localhost"
        port = 8888
        while True:
            _in = input(f'choose a host and port (current={addr}:{port}): ').split(":")
            if _in[0] == "":
                break
            addr = _in[0]
            port = int(_in[1])
        self.socket.connect((addr,port))
    def sendpos(self):
        while True:
            self.socket.send(f'{self.player.x}:{self.player.y}'.encode("utf-8"))
            sleep(1)

if __name__ == "__main__":
    c = Client()
    c.sendpos()