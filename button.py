# custom button class for filters
from touch import Button
from picovector import Polygon

class CustomButton:
    def __init__(self, x, y, w, h, label, filter_data, colours):
        self.button = Button(x, y, w, h)
        self.bounds = (x, y, w, h)
        self.label = label
        self.filter = filter_data
        self.colours = colours
        self.poly = Polygon().rectangle(x, y, w, h, (10, 10, 10, 10))

    def draw(self, display, vector, touch, selected):
        if self == selected:
            display.set_pen(self.colours["BUTTON_SELECTED"])
        else:
            display.set_pen(self.colours["BUTTON_BG"])
        vector.draw(self.poly)

        text_colour = display.create_pen(255, 255, 255)
        display.set_pen(self.colours["WHITE"])
        vector.set_font_size(32)
        
        x, y, width, height = (vector.measure_text(self.label))
        x = int(self.bounds[0] + (self.bounds[2] - width) / 2)
        y = int(self.bounds[1] + (self.bounds[3] - height))
        vector.text(self.label, x, y)
        
    def is_pressed(self):
        return self.button.is_pressed()