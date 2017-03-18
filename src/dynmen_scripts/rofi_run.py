from dynmen.rofi import Rofi
from Xlib.display import Display

def get_min_resolution(display):
    n_screens = display.screen_count()
    heights = set()
    for idx in range(n_screens):
        screen = display.screen(idx)
        heights.add(screen['height_in_pixels'])
    return min(heights)

def launch_rofi(show, *other_modi):
    from os import getenv, _exit
    modi = (show,) + other_modi

    menu = Rofi()
    menu.dmenu = False
    menu.threads = 0
    menu.fullscreen = True
    menu.font = 'Dejavu Sans Mono 14'
    menu.color_window = "argb:dc222222, #fac863, #fac863"
    menu.color_normal = "argb:0000000, #ffffff, argb:0000000, #fac863, #1b2b34"
    menu.color_active = "argb:0000000, #6699cc, argb:0000000, #6699cc, #1b2b34"
    menu.color_urgent = "argb:0000000, #f99157, argb:0000000, #f99157, #1b2b34"
    menu.monitor = -1
    menu.modi = ','.join(modi)
    menu.show = show
    menu.pid = '/tmp/rofi_{}'.format(getenv('USER', 'nouser'))

    display = Display(getenv('DISPLAY', ':0'))
    menu.padding = int(get_min_resolution(display) / 4)

    menu()
    display.close()
    _exit(0)

def main_run():
    launch_rofi('run', 'drun', 'window')

def main_window():
    launch_rofi('window', 'run', 'drun')

