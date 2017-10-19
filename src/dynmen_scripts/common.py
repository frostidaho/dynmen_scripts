def get_rofi(prompt='Launch: '):
    from dynmen.rofi import Rofi
    "Get a rofi menu object with my usual settings"
    menu = Rofi()
    menu.font = 'Dejavu Sans Mono 14'
    # menu.color_window = "argb:dc222222, #fac863, #fac863"
    # menu.color_normal = "argb:0000000, #ffffff, argb:0000000, #fac863, #1b2b34"
    # menu.color_active = "argb:0000000, #6699cc, argb:0000000, #6699cc, #1b2b34"
    # menu.color_urgent = "argb:0000000, #f99157, argb:0000000, #f99157, #1b2b34"
    menu.monitor = -1
    # menu.separator_style = 'dash'
    menu.prompt = prompt
    menu.i = True
    return menu

def _make_get_min_res():
    from Xlib.display import Display
    from os import getenv
    def get_min_resolution(DISPLAY=None):
        if DISPLAY is None:
            DISPLAY = getenv('DISPLAY', ':0')
        display = Display(DISPLAY)
        try:
            n_screens = display.screen_count()
            heights = set()
            for idx in range(n_screens):
                screen = display.screen(idx)
                heights.add(screen['height_in_pixels'])
            return min(heights)
        finally:
            display.close()
    return get_min_resolution
get_min_resolution = _make_get_min_res()

