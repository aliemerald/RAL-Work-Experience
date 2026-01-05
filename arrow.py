# arrow class for up and down buttons to set speed
from touch import Button
from picovector import Polygon, Transform

class Arrow:
    def __init__(self, x, y, r, colours, point_up=True):
        w = h = 2 * r
        self.button = Button(x, y, w, h)
        self.bounds = (x, y, w, h)
        self.colours = colours
        self.center = (x + r, y + r)

        self.poly = Polygon().regular(*self.center, r, 3)

        self.point_up = point_up

    def draw(self, display, vector, touch, selected):
        if self == selected:
            display.set_pen(self.colours["BUTTON_SELECTED"])
        else:
            display.set_pen(self.colours["BUTTON_BG"])

        transform = Transform()
        if self.point_up:
            transform.rotate(180, self.center)

        vector.set_transform(transform)
        vector.draw(self.poly)
        vector.set_transform(Transform())

    def is_pressed(self):
        return self.button.is_pressed()
