import PVector as v
import arcade
import math

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Seeting Behavior!"

class Ship:
    def __init__(self):
        self.location = v.PVector(250,200)
        self.velocity = v.PVector(0,0)
        self.acceleration = v.PVector(0,0)
        self.max_speed = 0
        self.desired = v.PVector(0,0)
        self.target = v.PVector(400,300)

    def update(self):
        self.desired = self.location.sub(self.target)
        #self.desired.normalize(self.desired)
        #self.desired.mult(self.max_speed)
        print(self.desired.__str__())

    def draw(self):
        arcade.draw_circle_filled(self.location.x, self.location.y, 20, arcade.color.RED)


class Screen(arcade.Window):

    def __init__(self):

        # Call the parent class's init function
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.ASH_GREY)

        self.ship = Ship()

    def on_draw(self):
        arcade.start_render()
        self.ship.update()
        self.ship.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        pass

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