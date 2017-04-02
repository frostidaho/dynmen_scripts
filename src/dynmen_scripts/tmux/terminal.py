from .common import NO_PANE, Register
from . import templates
from itertools import chain
import subprocess as _sp
from shutil import which as _which
from functools import partial as _partial

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


class TerminalAttach(TerminalLauncher):
    def __call__(self, pane_info, directory=None):
        files = []
        # add = files.append
        tl = templates
        if pane_info == NO_PANE:
            files.extend(tl.tmux_attach(directory))
        else:
            d_pane = pane_info._asdict()
            d_pane['directory'] = directory
            files.extend(tl.tmux_source(**d_pane))
            # cmds_file = tl.tmux_commands_attach(**d_pane)
            # add(tl.tmux_source(cmds_file.name))
            # add(cmds_file)
        return super().__call__(*files)

