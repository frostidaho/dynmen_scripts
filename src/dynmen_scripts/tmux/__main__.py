from .ctrl import get_panes, kill_pane, new_session
from .common import NO_PANE, HOME_DIR
from .terminal import TerminalAttach
from functools import partial
from collections import OrderedDict
from ..common import get_rofi

def _make_get_display_dict():
    from tabulate import tabulate
    display_template = OrderedDict()
    display_template['Session'] = '{session_name} ({session_id})'
    display_template['Path'] = '{path}'
    display_template['Cmd'] = '{pane_current_command}'
    display_template['Window/Pane'] = '{window_index}/{pane_index}'
    display_template_vals = tuple(display_template.values())
    def get_display_dict(panes):
        template = display_template_vals
        display = []
        for pane in panes:
            d = pane._asdict()
            d['path'] = d['pane_current_path'].replace(HOME_DIR, '~')
            display.append([x.format(**d) for x in template])
        display = tabulate(display, tablefmt='plain').splitlines()
        display = ['\t'+x for x in display]
        return OrderedDict(zip(display, panes))
    return get_display_dict
get_display_dict = _make_get_display_dict()


def query(menu, prompt):
    menu.prompt = prompt
    menu.lines = 1
    res = menu()
    return res.selected

def query_new_session(menu, attach, systemd=False):
    name = query(menu, 'New session name: ').strip()
    new_session(name, systemd)
    panes = [x for x in get_panes() if x.session_name == name]
    attach(panes[0])

def query_kill_pane(menu):
    menu.prompt = 'Select pane to kill: '
    panes = get_panes()
    while panes:
        display_dict = get_display_dict(panes)
        res = menu(display_dict)
        pane_info = res.value
        kill_pane(pane_info)
        panes = get_panes()


def main():
    menu = get_rofi()
    menu.fullscreen = True

    part = partial

    pre = OrderedDict()
    attach = TerminalAttach()
    pre['• Attach to last session (or spawn one if none exist)'] = part(attach, NO_PANE)
    post = OrderedDict()

    post['• Create session'] = part(query_new_session, menu, attach, False)
    post['• Create persistent session'] = part(query_new_session, menu, attach, True)
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

