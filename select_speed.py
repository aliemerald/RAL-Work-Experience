# max RPM = 2100 so highest Hz is actually only 35 but range of Hz input is 0-299
# with filter move disk max RPM ~ 1540
from touch import Button
from picovector import Polygon
from arrow import Arrow
import utime

class SpeedSelect:
    def __init__(self, touch, display, vector, colours, dr):
        self.display = display
        self.vector = vector
        self.touch = touch
        self.colours = colours
        self.dr = dr
        self.buttons = []
        self.hundreds = 0
        self.tens = 0
        self.units = 0
        self.make_buttons()
        
        self.speed_set = False
        self.running = False
        self.first_time = True

        self.set_button = Button(160, 200, 70, 30)
        self.set_rect = Polygon().rectangle(160, 200, 70, 30, (5, 5, 5, 5))

        self.start_button = Button(10, 200, 60, 30)
        self.start_rect = Polygon().rectangle(10, 200, 60, 30, (5, 5, 5, 5))

        self.background_rect = Polygon().rectangle(0, 0, 240, 240, (10, 10, 10, 10))

    def make_buttons(self):
        WIDTH, HEIGHT = self.display.get_bounds()
        size = WIDTH // 18
        padding = 40
        col_gap = 40

        start_y_up = 65
        start_y_down = 160

        for i in range(6):
            col = i % 3
            row = i // 3
            x = padding + col * (2 * size + col_gap)
            y = start_y_up if row == 0 else start_y_down
            point_up = row == 0

            arrow = Arrow(x, y, size, self.colours, point_up=point_up)
            self.buttons.append(arrow)

    def draw(self):
        self.display.set_pen(self.colours["BLACK"])
        self.display.clear()

        self.display.set_pen(self.colours["BG"])
        self.vector.draw(self.background_rect)

        self.update_digits()

        for bttn in self.buttons:
            is_pressed = bttn.is_pressed()
            bttn.draw(self.display, self.vector, self.touch, bttn if is_pressed else None)

        WIDTH, HEIGHT = self.display.get_bounds()
        size = 60
        padding = 25
        col_gap = 5

        digit_values = [self.hundreds, self.tens, self.units]
        for i, value in enumerate(digit_values):
            x = int(padding + i * (size + col_gap))
            y = 95
            box = Polygon().rectangle(x, y, size, size, (4, 4, 4, 4))
            self.display.set_pen(self.colours["BUTTON_BG"])
            self.vector.draw(box)
            self.display.set_pen(self.colours["WHITE"])
            self.vector.set_font_size(48)
            text = str(value)
            _, _, width, height = (self.vector.measure_text(text))
            tx = int(x + (size - width) // 2 - 1)            
            ty = int(y + (size - height)+12)
            self.vector.text(text, tx, ty)

        self.display.set_pen(self.colours["WHITE"])
        self.vector.set_font_size(32)
        title = "SPEED (Hz)"
        _, _, width, height = (self.vector.measure_text(title))
        tx = int((WIDTH - width) // 2)
        ty = int(20 + height)
        self.vector.text(title, tx, ty)

        self.display.set_pen(self.colours["BUTTON_BG"])
        self.vector.draw(self.set_rect)
        self.display.set_pen(self.colours["WHITE"])
        self.vector.set_font_size(20)
        self.vector.text("Set", 180, 220)

        self.touch.poll()

        if self.set_button.is_pressed():
            while self.set_button.is_pressed():
                self.touch.poll()
            self.display.set_pen(self.colours["BUTTON_SELECTED"])
        else:
            self.display.set_pen(self.colours["BUTTON_BG"])
        self.vector.draw(self.set_rect)

        self.display.set_pen(self.colours["WHITE"])
        if self.speed_set:
            label = "Change"
            self.vector.text(label, 165, 220)
        else:
            label = "Set"
            self.vector.text(label, 180, 220)       

        if self.speed_set:
            if self.running:
                btn_label = "Stop"
            else:
                btn_label = "Start"
            btn_rect = self.start_rect
            if self.start_button.is_pressed():
                while self.start_button.is_pressed():
                    self.touch.poll()
                self.display.set_pen(self.colours["BUTTON_SELECTED"])
            else:
                self.display.set_pen(self.colours["BUTTON_BG"])
            self.vector.draw(btn_rect)
            self.display.set_pen(self.colours["WHITE"])
            self.vector.text(btn_label, 20, 220)


    def update_digits(self):
        self.touch.poll()
        if self.first_time or not self.speed_set:
            for i, arrow in enumerate(self.buttons):
                if arrow.is_pressed():
                    column = i % 3 
                    is_up = arrow.point_up
                    if column == 0:
                        if is_up:
                            self.hundreds = (self.hundreds + 1) % 3  # cap at 2
                        else:
                            self.hundreds = (self.hundreds - 1) % 3
                    elif column == 1:
                        if is_up:
                            self.tens = (self.tens + 1) % 10
                        else:
                            self.tens = (self.tens - 1) % 10
                    elif column == 2:
                        if is_up:
                            self.units = (self.units + 1) % 10
                        else:
                            self.units = (self.units - 1) % 10

        if self.set_button.is_pressed():
            if not self.speed_set:
                self.speed_set = True
                self.first_time = False
                speed = self.hundreds * 100 + self.tens * 10 + self.units
                print(f"speed set to {speed} Hz")
                self.dr.roller.set_speed(speed * 60 * 100)
            else:
                if self.running:
                    self.running = False
                    self.dr.stop()
                    print("disk stopped")
                self.speed_set = False

        if self.speed_set:
            if self.start_button.is_pressed():
                if not self.running:
                    self.running = True
                    self.dr.start()
                    utime.sleep(2)
                    actual_spd = self.dr.roller.get_speed()
                    print(f"disk rotating at {actual_spd} RPM")
                else:
                    self.running = False
                    self.dr.stop()
                    print("disk stopped")
                    