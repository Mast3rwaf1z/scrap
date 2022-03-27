from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

buffer = 1024

class Host():
    clients:list[tuple[socket, int, int]] = []
    def __init__(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.bind(("localhost", 8888))
    def connection(self):
        self.socket.listen()
        client, addr = self.socket.accept()
        self.clients = Thread(target=self.handle, args=(client,)).start(), 0, 0
    def handle(self, client:socket):
        while True:
            recv = bytes.decode(client.recv(buffer), "utf-8")
            if recv[:3] == "pos":
                for _client in self.clients:
                    if _client[0] == client:
                        client[1] = recv[3:].split("x")[0]
                        client[2] = recv[3:].split("x")[1]
                        print(f'x pos: {client[1]}')
                        print(f'y pos: {client[2]}')
                        break
            sleep(1)

if __name__ == "__main__":
    h = Host()
    h.connection()