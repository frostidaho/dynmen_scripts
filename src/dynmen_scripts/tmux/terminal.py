from weakref import WeakValueDictionary as _WeakValueDictionary
from weakref import WeakSet as _WeakSet
from .common import NO_PANE, FileInfo
from itertools import chain
import subprocess as _sp
from shutil import which as _which
from functools import partial as _partial

class Register:
    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        if "_instances" not in cls.__dict__:
            cls._instances = _WeakSet()
        cls._instances.add(instance)
        return instance

    def __init__(self, name):
        self.name = name
        self.registered = _WeakValueDictionary()
        self.default = None

    def __getitem__(self, key):
        return self.registered[key]

    def __call__(self, fn, name='', default=False):
        if not name:
            name = fn.__name__
        if self.default is None:
            self.default = name
        elif default:
            self.default = name
        self.registered[name] = fn
        return fn

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name
        dflt = self.default
        return '<{cname}({name!r}): default -> {dflt}>'.format(**locals())


register_terminal = Register('terminal')

def _maybe_register(executable, **kw):
    if _which(executable):
        return _partial(register_terminal, **kw)
    else:
        def wrapper(fn, *args, **kwargs):
            return fn
        return wrapper

@_maybe_register('xfce4-terminal')
def xfce4(script_path):
    cmd = [
        'xfce4-terminal',
        '--show-borders',
        '--maximize',
        '--command={}'.format(script_path),
    ]
    return cmd

@_maybe_register('alacritty', default=True)
def alacritty(script_path):
    return ['alacritty', '-e', script_path]

def _make_scripts():
    import os
    import stat
    from collections import OrderedDict
    from contextlib import contextmanager
    from tempfile import TemporaryDirectory
    

    @contextmanager
    def scripts(main_file, *files):
        S_IEXEC = stat.S_IEXEC
        files = main_file, *files
        d = OrderedDict()
        path_join = os.path.join
        with TemporaryDirectory() as td:
            for file_info in chain([main_file], files):
                path = path_join(td, file_info.name)
                with open(path, mode='w') as fobj:
                    fobj.write(file_info.contents)
                if file_info.executable:
                    st = os.stat(path)
                    os.chmod(path, st.st_mode | S_IEXEC)
            yield td, main_file.name
    return scripts
scripts = _make_scripts()


class TerminalLauncher:
    register_terminal = register_terminal
    def __init__(self, backend=''):
        rt = self.register_terminal
        if isinstance(backend, str):
            if backend:
                fn = rt[backend]
            else:
                fn = rt[rt.default]
        else:
            fn = backend
        self.backend = fn

    def __call__(self, main_file, *files):
        with scripts(main_file, *files) as script_info:
            path, name = script_info
            cmd = self.backend('./'+name)
            sp = _sp
            run, DEVNULL = sp.run, sp.DEVNULL
            res = run(cmd, cwd=path, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
            return res.returncode


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

class TerminalAttach(TerminalLauncher):
    def __call__(self, pane_info):
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
        return super().__call__(*files)



