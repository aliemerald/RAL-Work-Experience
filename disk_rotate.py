# disk_rotate.py by Almond Zhao :)
from presto import Presto
from picovector import ANTIALIAS_BEST, PicoVector, Polygon, Transform

from colours import get_colours
from filters import filters
from select_speed import SpeedSelect
from RollerCanFunctions import DiskRotate

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

dr = DiskRotate()
speed_select = SpeedSelect(presto.touch, display, vector, colours, dr)
dr.stop()

while True:
    presto.touch.poll()
    display.set_pen(colours["BLACK"])
    display.clear()
    
    speed_select.draw()

    presto.update()
