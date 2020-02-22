from socket import *
from threading import Thread
import os,sys
import time

HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST,PORT)
FTP = '/home/tarena/FTP/'

class FTPServer(Thread):
    def __init__(self,connfd):
        super().__init__()
        self.connfd = connfd
    def do_list(self):
        files = os.listdir(FTP)
        if not files:
            self.connfd.send('kong'.encode())
            return
        else:
            self.connfd.send(b'ok')
            time.sleep(0.1)
        filelist = ''
        for file in files:
            filelist += file + '\n'
        self.connfd.send(filelist.encode())
    def do_get(self,filename):
        try:
            f = open(FTP+filename,'rb')
        except Exception:
            self.connfd.send('wu'.encode())
            return
        else:
            self.connfd.send(b'ok')
            time.sleep(0.1)
        while True:
            data = f.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
    def do_put(self,filename):
        if os.path.exists(FTP + filename):
            self.connfd.send('zai'.encode())
            return
        else:
            self.connfd.send(b'ok')
        f = open(FTP+filename,'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()
    def run(self):
        while True:
            request = self.connfd.recv(1024).decode()
            if not request or request == 'Q':
                return
            elif request == 'L':
                self.do_list()
            elif request[0] == 'G':
                filename = request.split(' ')[-1]
                self.do_get(filename)
            elif request == 'P':
                filename = request.split(' ')[-1]
                self.do_put(filename)
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)















