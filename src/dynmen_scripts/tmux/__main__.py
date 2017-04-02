from .info import get_tmux_panes
from .common import NO_PANE
from .terminal import TerminalAttach
from functools import partial
from collections import OrderedDict


from ..common import get_rofi
menu = get_rofi()
menu.fullscreen = True

def main():
    part = partial

    pre = OrderedDict()
    attach = TerminalAttach()
    pre['• Attach to last session (or spawn one if none exist)'] = part(attach, NO_PANE)
    post = OrderedDict()

    post['• Create session'] = part(query_new_session, menu, False)
    post['• Create persistent session'] = part(query_new_session, menu, True)
    post['• Kill pane'] = part(query_kill_pane, menu)

    panes = get_panes()
    total = OrderedDict()
    total.update(pre)

    if panes:
        display_dict = get_display_dict(panes)
    else:
        display_dict = {}
    for k,v in display_dict.items():
        total[k] = part(attach, v)
    total.update(post)
    res = menu(total).value()
    return 0

