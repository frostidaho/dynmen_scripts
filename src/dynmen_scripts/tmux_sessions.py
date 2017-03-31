from subprocess import run, PIPE, DEVNULL
from collections import namedtuple, OrderedDict
from tabulate import tabulate
from os import path, chdir
from functools import partial
from contextlib import contextmanager
from .utils import scripts, FileInfo

HOME_DIR = path.expanduser('~')
chdir(HOME_DIR)
PaneInfo = namedtuple(
    'PaneInfo',
    (
        'session_id',
        'window_index',
        'pane_index',
        'pane_current_path',
        'pane_current_command',
        'session_name',
        'pane_title',
        'window_name',
    ),
)

def _make_get_panes():
    pane_format_sep = " !@^@! "
    pane_format = pane_format_sep.join(('#{{{}}}'.format(x) for x in PaneInfo._fields))
    cmd = ['tmux', 'list-panes', '-a', '-F', pane_format]
    def get_panes():
        sep = pane_format_sep
        res = run(cmd, stdout=PIPE)
        lines = res.stdout.decode().splitlines()
        lines = [x.split(sep) for x in lines]
        make = PaneInfo._make
        return [make(x) for x in lines]
    return get_panes
get_panes = _make_get_panes()

tty_script_template = """
#!/usr/bin/sh
tmux source "$PWD/{tmux_file}"
"""

tmux_commands_template = '''
attach -t "{session_id}"
select-window -t "{window_index}"
select-pane -t {pane_index}
'''

tmux_attach_template = """
#!/usr/bin/sh
cd ~/
tmux attach || systemd-run --scope --user tmux new -s default
"""

NO_PANE = PaneInfo._make((None for i in range(len(PaneInfo._fields))))


def attach(pane_info):
    files = []
    add = files.append
    if pane_info == NO_PANE:
        files.append(FileInfo('torun', tmux_attach_template, True))
    else:
        d_pane = pane_info._asdict()
        tmux_file = 'tmuxcmds.conf'
        d_pane['tmux_file'] = tmux_file
        add(FileInfo('torun', tty_script_template.format(**d_pane), True))
        add(FileInfo(tmux_file, tmux_commands_template.format(**d_pane), False))
    with scripts(*files) as script_info:
        path, name = script_info
        cmd = [
            'xfce4-terminal',
            '--show-borders',
            '--maximize',
            '--command=./{}'.format(name),
        ]
        res = run(cmd, cwd=path, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
        return res.returncode

def _make_get_display_dict():
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

def new_session(name, systemd=False):
    cmd = ['tmux', 'new-session', '-d', '-s', name]
    if systemd:
        systemd_cmd = ['systemd-run', '--scope', '--user']
        systemd_cmd.extend(cmd)
        return run(systemd_cmd)
    return run(cmd)

def kill_pane(pane_info):
    d = pane_info._asdict()
    fmt = '{session_id}:{window_index}.{pane_index}'
    cmd = ['tmux', 'kill-pane', '-t', fmt.format(**d)]
    return run(cmd)

def query(menu, prompt):
    menu.prompt = prompt
    menu.lines = 1
    res = menu()
    return res.selected

def query_new_session(menu, systemd=False):
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

def _make_main():
    from .common import get_rofi
    menu = get_rofi()
    menu.fullscreen = True
    part = partial

    pre = OrderedDict()
    pre['• Attach to last session (or spawn one if none exist)'] = part(attach, NO_PANE)
    post = OrderedDict()

    post['• Create session'] = part(query_new_session, menu, False)
    post['• Create persistent session'] = part(query_new_session, menu, True)
    post['• Kill pane'] = part(query_kill_pane, menu)

    def main():
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
    return main
main = _make_main()

