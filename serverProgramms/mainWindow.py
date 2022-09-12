import sys
import sqlite3
import socket


class BDServer:
    def __init__(self, address):
        self.serverAddress = address

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.serverAddress)

        self.server.listen(10)
        self.getNewHosts()

    def getNewHosts(self):
        while True:
            clientSoc, clientAddress = self.server.accept()
            print(f"!new host!, address:{clientAddress}")
            clientSoc.send("connecting successful!".encode('utf-8'))
            request = clientSoc.recv(1024).decode('utf-8')
            answer = doingRequests(request)


def doingRequests(request):

    return ''


if __name__ == '__main__':
    server = BDServer(('192.168.100.18', 1410))
