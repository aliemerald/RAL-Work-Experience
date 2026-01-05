# menu screen for filter_move
from button import CustomButton
from filters import filters
from touch import Button
from picovector import Polygon

class MenuScreen:
    def __init__(self, touch, display, vector, colours):
        self.display = display
        self.vector = vector
        self.touch = touch
        self.colours = colours
        self.buttons = []
        self.make_buttons()

        self.selected_button = self.buttons[0]
        self.temp_selection = None
        self.change_enabled = False

        self.change_button = Button(50, 200, 140, 30)
        self.change_rect = Polygon().rectangle(55, 200, 120, 30, (6, 6, 6, 6))
        self.background_rect = Polygon().rectangle(0, 0, 240, 240, (10, 10, 10, 10))

    def make_buttons(self):
        WIDTH, HEIGHT = self.display.get_bounds()
        CX = WIDTH // 2
        CY = HEIGHT // 2
        size = CX // 2 - 4
        gap = size + 3

        for i, filter_data in enumerate(filters):
            col = i % 4
            row = i // 4
            x = 3 + col * gap
            y = CY - size + row * (size + 3)
            bttn = CustomButton(x, y, size, size, filter_data["element"], filter_data, self.colours)
            self.buttons.append(bttn)

    def draw(self):
        self.display.set_pen(self.colours["BLACK"])
        self.display.clear()

        self.display.set_pen(self.colours["BG"])
        self.vector.draw(self.background_rect)

        for bttn in self.buttons:
            if self.change_enabled:
                highlight = self.temp_selection
            else:
                highlight = self.selected_button
            bttn.draw(self.display, self.vector, self.touch, highlight)

        WIDTH, HEIGHT = self.display.get_bounds()
        self.display.set_pen(self.colours["WHITE"])
        self.vector.set_font_size(32)
        title = "MENU"
        _, _, width, height = (self.vector.measure_text(title))
        x = int((WIDTH - width) // 2)
        y = int(20 + height)
        self.vector.text(title, x, y)

        if self.change_enabled:
            button_colour = self.colours["BUTTON_SELECTED"]
        else:
            button_colour = self.colours["BUTTON_BG"]
        self.display.set_pen(button_colour)
        self.vector.draw(self.change_rect)

        self.display.set_pen(self.colours["WHITE"])
        self.vector.set_font_size(20)
        self.vector.text("Change Filter", 65, 220)

    def update(self):
        if self.change_button.is_pressed():
            self.change_enabled = True
            self.temp_selection = self.selected_button

        if self.change_enabled:
            for bttn in self.buttons:
                if bttn.is_pressed():
                    self.temp_selection = bttn
                    return "detail"
        return None

    def confirm_selection(self):
        if self.temp_selection:
            self.selected_button = self.temp_selection
        self._reset_selection_state()

    def cancel_selection(self):
        self._reset_selection_state()

    def _reset_selection_state(self):
        self.temp_selection = None
        self.change_enabled = False

    def get_selected_filter(self):
        active_button = self.temp_selection if self.temp_selection else self.selected_button
        if active_button:
            return active_button.filter
        return None