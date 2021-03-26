import socket
import sys
from struct import *
from .tornado_handlers import *

#La RaspBerru pi Tiene la ip 192.168.1.40
UDP_IP = "192.168.1.40"
RUDP_IP = "127.0.0.1"
RUDP_PORT = 5001
UDP_PORT = 5005
MESSAGE = "Connected"

r_data = {}

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def UPD_Connect():
    sock.connect((UDP_IP, UDP_PORT))

def toM(v):
	if v > 0:
		return int(abs(v)*1000)
	if v < 0:
		return int(abs(v)*999+1001)
	if v == 0:
		return int(2) #falta ver aqui que valor mandar

def sendC(i,v):
    BYTES = pack('BBBBBB',0,i,1,int(v/254+1),int(v%254+1),255)
    try:
        sock.sendto(BYTES, (UDP_IP, UDP_PORT))
        #ser.write(BYTES)
        s = unpack('BBBBBB',BYTES)
        #print(str(s))
        print(str(s))
    except:
        print ("nada")

def sendJson(data):
    #sock.sendto(bytes(data, "utf-8"), (UDP_IP, UDP_PORT))
    data

def sendData(key):
    if key == 'i':
        sendC(1,toM(0.35))
        sendC(3,toM(0.35))
        
    elif key == 'k':
        sendC(1,toM(-0.35))
        sendC(3,toM(-0.35))
    elif key == 'l':
        sendC(1,toM(0.35))
        sendC(3,toM(-0.35))
    elif key == 'j':
        sendC(1,toM(-0.35))
        sendC(3,toM(0.35))
    else:
        sendC(1,toM(0))
        sendC(3,toM(0))


class upr_socket:
    ''' 
    class to comunicate the robot by udp socket
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock;

    def connect(self, host, port):
        self.sock.connect((host,port))

    def send_info(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)