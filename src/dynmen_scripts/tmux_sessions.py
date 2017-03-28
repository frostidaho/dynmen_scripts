# from dynmen.rofi import Rofi
# from subprocess import run, PIPE
# from collections import namedtuple
# from tabulate import tabulate
# from os import path

# HOME_DIR = path.expanduser('~')
# PaneInfo = namedtuple(
#     'PaneInfo',
#     (
#         'session_id',
#         'window_index',
#         'pane_index',
#         'pane_current_path',
#         'pane_current_command',
#         'session_name',
#     ),
# )

# def get_panes():
#     sep = " !@^@! "
#     cmd = ['tmux', 'list-panes', '-a', '-F']
#     info = PaneInfo._fields
#     args = ['#{{{}}}'.format(x) for x in info]
#     args = sep.join(args)
#     cmd.append(args)
#     res = run(cmd, stdout=PIPE)
#     lines = res.stdout.decode().splitlines()
#     lines = [x.split(sep) for x in lines]
#     make = PaneInfo._make
#     return [make(x) for x in lines]

# x = get_panes()
# print()
# print(tabulate(x, headers=PaneInfo._fields))
# def get_display_dict():
#     d = {}
#     panes = get_panes()
#     display = []
#     for pane in panes:
#         session = '{} ({})'.format(pane.session_name, pane.session_id)
#         path = pane.pane_current_path
#         path = path.replace(HOME_DIR, '~')
#         cmd = pane.pane_current_command
#         idx = '{}/{}'.format(pane.pane_index, pane.window_index)
#         total = [session, path, cmd, idx]
#         display.append(total)
#         # d['\t'.join(total)] = pane
#     display = tabulate(display, tablefmt='plain').strip().splitlines()
#     return dict(zip(display, panes))
#     # return d

# def main():
#     from os import _exit
#     menu = Rofi()
#     menu.font = 'Dejavu Sans Mono 14'
#     menu.color_window = "argb:dc222222, #fac863, #fac863"
#     menu.color_normal = "argb:0000000, #ffffff, argb:0000000, #fac863, #1b2b34"
#     menu.color_active = "argb:0000000, #6699cc, argb:0000000, #6699cc, #1b2b34"
#     menu.color_urgent = "argb:0000000, #f99157, argb:0000000, #f99157, #1b2b34"
#     menu.monitor = -1
#     menu(get_display_dict())
#     # _exit(0)

