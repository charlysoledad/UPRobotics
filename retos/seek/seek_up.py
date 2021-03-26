import arcade
import math
import numpy as np
from random import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Seek for Autonomous Vehicle"

MAX_SPEED = 5

class Vector():
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __set__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        self.x += v.x
        self.y += v.y

    def __sub__(self, v):
        self.x -= v.x
        self.y -= v.y

    def __vsub__(self, v1, v2):
        self.set(v1.x - v2.x, v1.y - v2.y)

    def __mult__(self, value):
        self.x *= value
        self.y *= value

    def __div__(self,value):
        self.x = self.x / value
        self.y = self.y / value

    def mag(self):
        return math.sqrt((self.x*self.x) + (self.y*self.y))

    def normalize(self):
        m = self.mag()
        if m != 0.0:
            self.__div__(m)


    def __limit__(self, value):
        if(self.mag() > value ):
            self.normalize()
            self.__mult__(value)
        return self

    @staticmethod
    def random( size=1 ):
        sizex = size
        sizey = size
        if isinstance(size, tuple) or isinstance(size, list):
            sizex = size[0]
            sizey = size[1]
        elif isinstance(size, Vector):
            sizex = size.x
            sizey = size.y
        return Vector(random() * sizex, random() * sizey)

class Ship(object):
    def __init__(self):
        self.position = Vector(randint(0,SCREEN_WIDTH), randint(0,SCREEN_WIDTH))
        self.velocity = Vector(0, 0)
        self.acceleration =  Vector(0, 0)
        self.desired  = Vector(0,0)
        self.m_pos = Vector(0,0)

    def update(self, mouse_pos):
        self.desired .__set__(mouse_pos.x - self.position.x, mouse_pos.y - self.position.y)
        self.desired .normalize()
        self.desired .__mult__(0.5)

        self.acceleration = self.desired

        self.velocity.__add__(self.acceleration)
        self.velocity.__limit__(MAX_SPEED)

        self.position.__add__(self.velocity)

        #print(str(self.acceleration.x) + " - " + str(self.acceleration.y))

    def set_mouse(self, v):
        self.m_pos = v

    def get_mouse(self):
        return self.m_pos

    def checkEdge(self):
        if (self.position.x > SCREEN_WIDTH) :
            self.position.x = 0
        elif (self.position.x < 0) :
            self.position.x = SCREEN_WIDTH
            
        if (self.position.y > SCREEN_HEIGHT) :
            self.position.y = 0
        elif (self.position.y < 0) :
            self.position.y = SCREEN_HEIGHT        

    def draw(self):
        arcade.draw_circle_filled(self.position.x, self.position.y, 20, arcade.color.RED)


class Screen(arcade.Window):

    def __init__(self):

        self.mouse_x = 0
        self.mouse_y = 0

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.ship = Ship()

    def on_draw(self):
        arcade.start_render()

        self.ship.update(self.get_mouse())
        self.ship.checkEdge()
        self.ship.draw()


    def get_mouse(self):
        return Vector(self.mouse_x, self.mouse_y)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.mouse_x = x
        self.mouse_y = y
        

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """ Called when a user releases a mouse button. """
        pass

def main():
    window = Screen()
    arcade.run()


if __name__ == "__main__":
    main()