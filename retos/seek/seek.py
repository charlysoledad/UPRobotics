import arcade
import math
from random import randint, uniform
from vec2 import Vec2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Seeting Behavior!"

MAX_SPEED = 5
MAX_FORCE = 0.1
_RADIUS = 120

class Ship(object):
    def __init__(self):
        self.position = Vec2(randint(0,SCREEN_WIDTH),randint(0, SCREEN_HEIGHT))
        self.velocity = Vec2(MAX_SPEED,0)
        self.acceleration = Vec2(0,0)
        self.mouse_position = Vec2(0,0)

    def update(self, pos_mouse):
        self.acceleration = self.seek(pos_mouse)
        self.velocity += self.acceleration

        if self.velocity.length() > MAX_SPEED:
            self.velocity.__rdiv__(MAX_SPEED)

        self.position += (self.velocity)
        if self.position.data[0] > SCREEN_WIDTH:
            self.position.data[0] = 0
        if self.position.data[0] < 0:
            self.position.data[0] = SCREEN_WIDTH
        if self.position.data[1] > SCREEN_HEIGHT:
            self.position.data[1] = 0
        if self.position.data[1] < 0:
            self.position.data[1] = SCREEN_HEIGHT
        
    def seek(self, target):
        self.desired = (target - self.position) 
        print(self.desired)
        dist = self.desired.length()
        self.desired.normalize()
        if dist < _RADIUS:
            self.desired *= dist / _RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED

        steer = (self.desired - self.velocity)

        if steer.length() > MAX_FORCE:
            steer.__rdiv__(MAX_FORCE)
        return steer

    def draw(self):
        arcade.draw_circle_filled(self.position.data[0], self.position.data[1], 20, arcade.color.RED)

class Screen(arcade.Window):

    def __init__(self):

        # Call the parent class's init function
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.position_mouse = Vec2(0,0)
        self.ship = Ship()

    def on_draw(self):
        arcade.start_render()

        self.ship.update(self.mouse_pos())
        self.ship.draw()

    def mouse_pos(self):
        return self.position_mouse

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.position_mouse = Vec2(x,y)
        

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

def main():
    window = Screen()
    arcade.run()


if __name__ == "__main__":
    main()