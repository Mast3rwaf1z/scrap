from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

buffer = 1024

class Host():
    x = 0
    y = 0
    def __init__(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.bind(("localhost", 8888))
    def connection(self):
        self.socket.listen()
        client, addr = self.socket.accept()
        Thread(target=self.handle, args=(client,)).start()
    def handle(self, client:socket):
        while True:
            recv = bytes.decode(client.recv(buffer), "utf-8")
            if recv[:3] == "pos":
                self.x = recv[3:].split("x")[0]
                self.y = recv[3:].split("x")[1]
            print(f'x pos: {self.x}')
            print(f'y pos: {self.y}')
            sleep(1)

if __name__ == "__main__":
    h = Host()
    h.connection()