from os import getenv, _exit
from dynmen.rofi import Rofi
from Xlib.display import Display

def get_min_resolution():
    disp = Display(getenv('DISPLAY', ':0'))
    n_screens = disp.screen_count()
    heights = set()
    for idx in range(n_screens):
        screen = disp.screen(idx)
        heights.add(screen['height_in_pixels'])
    # try:
    #     disp.close()
    # except:
    #     pass
    return min(heights)

def launch_rofi(show, *other_modi):
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
    # menu.modi = "run,drun"
    # menu.show = 'run'
    menu.padding = int(get_min_resolution() / 4)
    menu.pid = '/tmp/rofi_{}'.format(getenv('USER', 'nouser'))
    out = menu([])
    _exit(0)

def main_run():
    return launch_rofi('run', 'drun', 'window')

def main_window():
    return launch_rofi('window', 'run', 'drun')


