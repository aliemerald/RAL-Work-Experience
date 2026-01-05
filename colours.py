def get_colours(display):
    return {
        "BLACK": display.create_pen(0, 0, 0),
        "WHITE": display.create_pen(255, 255, 255),
        "BUTTON_BG": display.create_pen_hsv(0.8, 0.5, 0.7),
        "BUTTON_SELECTED": display.create_pen(198, 16, 107),
        "BG": display.create_pen_hsv(0.8, 0.7, 0.6),
    }
