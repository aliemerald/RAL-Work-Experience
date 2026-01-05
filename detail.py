# detail/info screen - element energies
from picovector import Polygon
from touch import Button

class DetailScreen:
    def __init__(self, touch, display, vector, colours):
        self.display = display
        self.vector = vector
        self.touch = touch
        self.colours = colours
        self.filter_data = None

        self.back_button = Button(5, 200, 70, 30)
        self.choose_button = Button(160, 200, 80, 30)

        self.back_rect = Polygon().rectangle(5, 200, 70, 30, (5, 5, 5, 5))
        self.choose_rect = Polygon().rectangle(160, 200, 75, 30, (5, 5, 5, 5))

        self.element_box = Polygon().rectangle(10, 65, 110, 110, (12, 12, 12, 12))
        self.background_rect = Polygon().rectangle(0, 0, 240, 240, (10, 10, 10, 10))

    def show(self, filter_data):
        self.filter_data = filter_data

    def draw(self):
        self.display.set_pen(self.colours["BLACK"])
        self.display.clear()

        self.display.set_pen(self.colours["BG"])
        self.vector.draw(self.background_rect)
        
        self.display.set_pen(self.colours["BUTTON_BG"])
        self.vector.draw(self.element_box)
        
        WIDTH, HEIGHT = self.display.get_bounds()

        self.display.set_pen(self.colours["WHITE"])
        self.vector.set_font_size(32)
        title = "INFO"
        _, _, width, height = (self.vector.measure_text(title))
        x = int((WIDTH - width) // 2)
        y = int(20 + height)
        self.vector.text(title, x, y)

        self.vector.set_font_size(60)
        _, _, width, height = (self.vector.measure_text(self.filter_data["element"]))
        x = int(10 + (110 - width) // 2)
        y = int(65 + (110 - height))
        self.vector.text(self.filter_data["element"], x, y)

        self.vector.set_font_size(24)
        props = ["ka", "kb", "la", "lb"]
        for i, p in enumerate(props):
            label = f"{p.upper()}:"
            value = f"{self.filter_data[p]:.2f}"
            y = 85 + i * 28
            self.vector.text(label, 135, y)
            self.vector.text(value, 175, y)

        self.display.set_pen(self.colours["BUTTON_BG"])
        self.vector.draw(self.back_rect)
        self.vector.draw(self.choose_rect)

        self.display.set_pen(self.colours["WHITE"])
        self.vector.set_font_size(20)
        self.vector.text("< Back", 15, 220)
        self.vector.text("Choose", 170, 220)

    def update(self):
        if self.back_button.is_pressed():
            while self.back_button.is_pressed():
                self.touch.poll()
            return "back"
        if self.choose_button.is_pressed():
            while self.choose_button.is_pressed():
                self.touch.poll()
            return "choose"
        return None
