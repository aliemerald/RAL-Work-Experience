# filter move by Almond Zhao :)
from presto import Presto
from picovector import ANTIALIAS_BEST, PicoVector, Polygon, Transform
from menu import MenuScreen
from detail import DetailScreen
from colours import get_colours
from filters import filters
from RollerCanFunctions import FilterMove

presto = Presto(ambient_light=True)
display = presto.display
vector = PicoVector(display)
vector.set_antialiasing(ANTIALIAS_BEST)
t = Transform()

vector.set_font("Roboto-Medium.af", 54)
vector.set_font_letter_spacing(100)
vector.set_font_word_spacing(100)
vector.set_transform(t)

WIDTH, HEIGHT = display.get_bounds()
colours = get_colours(display)

background_rect = Polygon().rectangle(0, 0, WIDTH, HEIGHT, (10, 10, 10, 10))

menu_screen = MenuScreen(presto.touch, display, vector, colours)
detail_screen = DetailScreen(presto.touch, display, vector, colours)

current_screen = "menu"

fm = FilterMove()
fm.roller.enable_motor()
offset = 2200
fm.roller.set_position(offset)
index = 0

while True:
    presto.touch.poll()
    display.set_pen(colours["BLACK"])
    display.clear()
    
    if current_screen == "menu":
        menu_screen.draw()
        result = menu_screen.update()
        if result == "detail":
            detail_screen.show(menu_screen.get_selected_filter())
            current_screen = "detail"

    elif current_screen == "detail":
        detail_screen.draw()
        result = detail_screen.update()
        if result == "back":
            menu_screen.cancel_selection()
            current_screen = "menu"
        elif result == "choose":
            menu_screen.confirm_selection()
            current_screen = "menu"
            selected_filter_data = menu_screen.get_selected_filter()
            for i, filter_data in enumerate(filters):
                if filter_data == selected_filter_data:
                    index = i   
            fm.roller.set_position(offset + 36000/8 * index)
            
    presto.update()
