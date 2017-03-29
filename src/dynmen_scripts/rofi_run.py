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
    from .common import get_rofi
    modi = (show,) + other_modi

    menu = get_rofi()
    menu.dmenu = False
    menu.threads = 0
    menu.fullscreen = True
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

