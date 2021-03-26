import arcade
import math
import numpy as np
from random import *

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Seek for Autonomous Vehicle"

MAX_SPEED = 12
MAX_FORCE = 4
MASS = 2
RADIUS = 100

MOB_TEXTURE = arcade.load_texture("images/ship.png")
MOB_SCALE = .4
MOB_EFFECT = arcade.load_texture("images/effect.png")

class Vector():
    def __init__(self, _x=0, _y=0):
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
        self.__set__(v1.x - v2.x, v1.y - v2.y)

    def __mult__(self, value):
        self.x *= value
        self.y *= value

    def __div__(self,value):
        self.x = self.x / value
        self.y = self.y / value

    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        m = self.mag()
        if m != 0:
            return self.__div__(m)
        else:
            return Vector(0,0)


    def __limit__(self, value):
        if(self.mag() > value*value ):
            self.normalize()
            self.__mult__(value)
        else:
            pass
    """
    @staticmethod
    def angle(v1, v2):
        return acos(v1.dotproduct(v2) / (v1.mag() * v2.mag()))
        
    @staticmethod
    def angleDeg(v1, v2):
        return Vector.angle(v1,v2) * 180.0 / pi
    """
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

class Ship():
    def __init__(self):
        #self.position = Vector(randint(0,SCREEN_WIDTH), randint(0,SCREEN_WIDTH))
        self.position = Vector(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.velocity = Vector(0, 0)
        self.acceleration =  Vector(0, -2)
        self.desired  = Vector(0,0)
        self.steer = Vector(0,0)
        self.force = Vector(0,0)
        self.m_pos = Vector(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.angle = 0
        self.r = MOB_TEXTURE.height
        self.max_speed = 12
        self.max_force = 4

    def update(self, target):
        self.angle = self.getAngle()
        self.m_pos = target
        #self.seek(target)
        self.arrive(target)
        self.velocity.__add__(self.acceleration)
        self.velocity.__limit__(self.max_speed)
        self.position.__add__(self.velocity)
        #self.getDistance()
        #self.getVelocity()
        self.getForce()
        self.acceleration.__mult__(0.0)

        #print(str(self.acceleration.x) + " - " + str(self.acceleration.y))

    def seek(self, target):
        self.desired.__set__(target.x - self.position.x, target.y - self.position.y)
        self.desired.normalize()
        self.desired.__mult__(self.max_speed)

        self.steer.__set__(self.desired.x - self.velocity.x, self.desired.y - self.velocity.y) 
        self.steer.__limit__(self.max_force)

        self.applyForce(self.steer)

    def arrive(self, target):
        self.desired.__set__(target.x - self.position.x, target.y - self.position.y)
        d = self.desired.mag()
        self.desired.normalize()
        if d < RADIUS:
            d = self.map(d, 0, RADIUS, 0, self.max_speed)
            self.desired.__mult__(d)
        else:
            self.desired.__mult__(self.max_speed)

        self.steer.__set__(self.desired.x - self.velocity.x, self.desired.y - self.velocity.y) 
        self.steer.__limit__(self.max_force)

        self.applyForce(self.steer)

    def applyForce(self, force):
        self.force.__set__(force.x / MASS, force.y / MASS )
        self.acceleration.__add__(force)
        
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
        arcade.draw_texture_rectangle(self.position.x, self.position.y-20, MOB_SCALE * MOB_TEXTURE.width,
                              MOB_SCALE * MOB_TEXTURE.height, MOB_TEXTURE, self.angle)
        #arcade.draw_circle_filled(self.position.x, self.position.y, 20, arcade.color.BLUEBERRY)
    def set_maxSpeed(self, max_s):
        self.max_speed = max_s
    
    def set_maxForce(self, max_f):
        self.max_force = max_f

    def getDistance(self):
        dx = self.position.x - self.m_pos.x
        dy = self.position.y - self.m_pos.y
        dist = float(math.sqrt(dx*dx + dy*dy))
        print(dist)

    def getVelocity(self):
        vel = float("{0:.2f}".format(self.velocity.mag()))
        return vel

    def getForce(self):
        force = float("{0:.2f}".format(self.steer.mag()))
        return force

    def getAngle(self):
        n_ang = math.atan2(self.velocity.y, self.velocity.x)
        tetha = n_ang + math.pi / 2
        angle = (tetha * 360.0) / (2 * math.pi)
        #angle = (n_ang * 180) / math.pi
        return angle

    def map(self, x, in_min, in_max, out_min, out_max):
        return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

    def separate(self, ships):
        desired_sep = self.r*2
        i_sum = Vector()
        count = int(0)
        for v in ships:
            dist = Vector(self.position.x - v.x, self.position.y - v.y)
            d = dist.mag()
            if((d > 0) and (d < desired_sep)):
                diff = Vector(self.position.x - v.x, self.position.y - v.y)
                diff.normalize()
                diff.__div__(d)
                i_sum.__add__(diff)
                count += 1

        if count > 0:
            i_sum.__div__(count)
            i_sum.normalize()
            i_sum.__mult__(self.max_speed)
            steer = Vector(self.i_sum.x - self.velocity.x, self.i_sum.y - self.velocity.y)
            steer.__limit__(self.max_force)
            self.applyForce(steer)

class Screen(arcade.Window):

    def __init__(self):

        self.mouse_x = 0
        self.mouse_y = 0

        # Call the parent class's init function
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.BLACK)

        self.ship = Ship()

        self.speed = MAX_SPEED
        self.force = MAX_FORCE

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_line(self.mouse_x, self.mouse_y, self.mouse_x-RADIUS, self.mouse_y ,arcade.color.WHITE, 2)
        arcade.draw_line(self.mouse_x, self.mouse_y, self.mouse_x+RADIUS, self.mouse_y ,arcade.color.WHITE, 2)
        arcade.draw_line(self.mouse_x, self.mouse_y, self.mouse_x, self.mouse_y+RADIUS ,arcade.color.WHITE, 2)
        arcade.draw_line(self.mouse_x, self.mouse_y, self.mouse_x, self.mouse_y-RADIUS ,arcade.color.WHITE, 2)
        arcade.draw_circle_outline(self.mouse_x, self.mouse_y, RADIUS, arcade.color.WHITE, 3)

        self.ship.update(self.get_mouse())
        self.ship.checkEdge()
        self.ship.draw()
        arcade.draw_text("Velocity: " + str(self.ship.getVelocity()) +"/" + str(float(self.speed)),
                         10, SCREEN_HEIGHT-20, arcade.color.WHITE, 12)
        arcade.draw_text("Force: " + str(self.ship.getForce()) +"/" + str(float(self.force)),
                         10, SCREEN_HEIGHT-40, arcade.color.WHITE, 12)
        arcade.draw_text("Angle: " + str(float("{0:.2f}".format(self.ship.getAngle()))) + " deg",
                         10, SCREEN_HEIGHT-60, arcade.color.WHITE, 12)
        arcade.draw_circle_filled(self.mouse_x, self.mouse_y, 4, arcade.color.WHITE)

    def get_mouse(self):
        return Vector(self.mouse_x, self.mouse_y)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # Forward/back
        if key == arcade.key.UP:
            self.speed += 1
        elif key == arcade.key.DOWN:
            self.speed -= 1
        if key == arcade.key.LEFT:
            self.force += 1
        elif key == arcade.key.RIGHT:
            self.force -= 1
            
        self.ship.set_maxSpeed(self.speed)
        self.ship.set_maxForce(self.force)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass

def main():
    window = Screen()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()