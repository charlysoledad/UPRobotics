import arcade
import socket
import sys
from struct import *


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

UDP_IP = "192.168.1.9"
RUDP_IP = "127.0.0.1"
RUDP_PORT = 5001
UDP_PORT = 5000
MESSAGE = "HI"

datos = ""

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
        s = unpack ('BBBBBB',BYTES)
        print(str(s))
    except:
        print ("nada")

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

class MyGame(arcade.Window):

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("left")
            sendC(1,toM(-0.35))
            sendC(3,toM(0.35))
        elif key == arcade.key.RIGHT:
            print("right")
            sendC(1,toM(0.35))
            sendC(3,toM(-0.35))
        elif key == arcade.key.UP:
            print("up")
            sendC(1,toM(0.35))
            sendC(3,toM(0.35))
        elif key == arcade.key.DOWN:
            print("down")
            sendC(1,toM(-0.35))
            sendC(3,toM(-0.35))

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            print("release")
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            print("release")


def main():
    window = MyGame(640, 480, "UP Robotics")
    arcade.run()


if __name__ == "__main__":
    main() 
