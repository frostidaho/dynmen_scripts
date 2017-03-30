from contextlib import contextmanager as _contextmanager
from subprocess import run as _run

_tty_script_template = """
#!/usr/bin/sh
tmux source '{tmux_commands_path}'
#{shell}
"""

_tmux_commands_template = '''
attach -t "{session_id}"
select-window -t "{window_index}"
select-pane -t {pane_index}
'''

@_contextmanager
def _attach_script(pane_info):
    from tempfile import TemporaryDirectory
    from stat import S_IEXEC
    from os import getenv, chmod, stat, path

    with TemporaryDirectory() as td:
        fpath = path.join(td, 'torun.tmux')
        fpath_torun = path.join(td, 'torun')

        with open(fpath, mode='w') as fscript:
            tmux_commands = _tmux_commands_template.format(**pane_info._asdict())
            fscript.write(tmux_commands)

        with open(fpath_torun, mode='w') as fscript:
            ttyscript = _tty_script_template.format(
                tmux_commands_path=fpath,
                shell=getenv('SHELL', 'bash'),
            )
            fscript.write(ttyscript)
        st = stat(fpath_torun)
        chmod(fpath_torun, st.st_mode | S_IEXEC)
        yield fpath_torun


# _guake_template = """
# #!/usr/bin/sh
# guake --select-tab 0\
#       --show\
#       --execute-command {script_path}
# """

class Attach:
    def __init__(self, backend='xfce4'):
        self.backend = backend

    def __call__(self, pane_info):
        fn = getattr(self, 'run_in_{}'.format(self.backend))
        with _attach_script(pane_info) as script_path:
            return fn(script_path)

    @staticmethod
    def run_in_xfce4(script_path):
        cmd = [
            'xfce4-terminal',
            '--show-borders',
            '--maximize',
            '--command={}'.format(script_path),
        ]
        return _run(cmd)

    @staticmethod
    def run_in_guake(script_path):
        cmd = [
            'guake',
            '--select-tab',
            '0',
            '--show',
            '--execute-command',
            script_path,
        ]
        return _run(cmd)

