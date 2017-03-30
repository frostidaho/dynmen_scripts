from subprocess import run, PIPE
from collections import namedtuple, OrderedDict
from tabulate import tabulate
from os import path, chdir
from functools import partial
from contextlib import contextmanager
# import re
# invis = r"\x1b\[\d+[;\d]*m|\x1b\[\d*\;\d*\;\d*m"
# tags = [invis, '<b>', '</b>', '<u>', '</u>', '<i>', '</i>']
# tab._invisible_codes = re.compile('|'.join(tags))

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
tmux source '{tmux_commands_path}'
#{shell}
"""

tmux_commands_template = '''
attach -t "{session_id}"
select-window -t "{window_index}"
select-pane -t {pane_index}
'''

@contextmanager
def attach_script(pane_info):
    from tempfile import TemporaryDirectory
    from stat import S_IEXEC
    from os import getenv, chmod, stat

    with TemporaryDirectory() as td:
        fpath = path.join(td, 'torun.tmux')
        fpath_torun = path.join(td, 'torun')

        with open(fpath, mode='w') as fscript:
            tmux_commands = tmux_commands_template.format(**pane_info._asdict())
            fscript.write(tmux_commands)

        with open(fpath_torun, mode='w') as fscript:
            ttyscript = tty_script_template.format(
                tmux_commands_path=fpath,
                shell=getenv('SHELL', 'bash'),
            )
            fscript.write(ttyscript)
        st = stat(fpath_torun)
        chmod(fpath_torun, st.st_mode | S_IEXEC)
        yield fpath_torun

def attach(pane_info):
    with attach_script(pane_info) as script_path:
        cmd = [
            'xfce4-terminal',
            '--show-borders',
            '--maximize',
            '--command={}'.format(script_path),
        ]
        return run(cmd)


class DisplayPanes(object):
    display_template = OrderedDict()
    display_template['Session'] = '{session_name} ({session_id})'
    display_template['Path'] = '{path}'
    display_template['Cmd'] = '{pane_current_command}'
    display_template['Window/Pane'] = '{window_index}/{pane_index}'
    display_template_vals = tuple(display_template.values())

    @classmethod
    def create_dict(cls, panes):
        template = cls.display_template_vals
        display = []
        for pane in panes:
            d = pane._asdict()
            d['path'] = d['pane_current_path'].replace(HOME_DIR, '~')
            display.append([x.format(**d) for x in template])
        display = tabulate(display, tablefmt='plain').strip().splitlines()
        return OrderedDict(zip(display, panes))
get_display_dict = DisplayPanes.create_dict

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
    
def main():
    from .common import get_rofi
    menu = get_rofi()
    menu.fullscreen = True

    panes = get_panes()
    d = OrderedDict()
    if panes:
        display_dict = get_display_dict(panes)
    else:
        display_dict = {}
    for k,v in display_dict.items():
        d[k] = partial(attach, v)
    
    d['• Create session'] = partial(query_new_session, menu, False)
    d['• Create persistent session'] = partial(query_new_session, menu, True)
    d['• Kill pane'] = partial(query_kill_pane, menu)
    res = menu(d)
    res2 = res.value()
    return 0

