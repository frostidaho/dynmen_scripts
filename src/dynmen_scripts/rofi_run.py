def launch_rofi(show, *other_modi):
    from os import getenv, _exit
    from .common import get_rofi, get_min_resolution
    modi = (show,) + other_modi
    menu = get_rofi()
    menu.dmenu = False
    menu.threads = 0
    menu.fullscreen = True
    menu.modi = ','.join(modi)
    menu.show = show
    menu.pid = '/tmp/rofi_{}'.format(getenv('USER', 'nouser'))
    menu.padding = int(get_min_resolution() / 4)
    menu()
    _exit(0)

def main_run():
    launch_rofi('run', 'drun', 'window')

def main_window():
    launch_rofi('window', 'run', 'drun')

