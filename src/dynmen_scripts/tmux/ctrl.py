from collections import namedtuple as _namedtuple
import subprocess as _sp

def _make_get_panes():
    from .common import PaneInfo
    sep = " !@^@! "
    pane_format = sep.join(('#{{{}}}'.format(x) for x in PaneInfo._fields))
    cmd = ['tmux', 'list-panes', '-a', '-F', pane_format]
    run, PIPE, DEVNULL = _sp.run, _sp.PIPE, _sp.DEVNULL
    make = PaneInfo._make
    def get_panes():
        "Return a PaneInfo object for each available tmux pane"
        lines = run(cmd, stdout=PIPE, stderr=DEVNULL, stdin=DEVNULL) \
                                 .stdout.decode().splitlines()
        return [make(x.split(sep)) for x in lines]
    return get_panes
get_panes = _make_get_panes()


def kill_pane(pane_info):
    "Kill the tmux pane corresponding to the given instance of PaneInfo"
    d = pane_info._asdict()
    fmt = '{session_id}:{window_index}.{pane_index}'
    cmd = ['tmux', 'kill-pane', '-t', fmt.format(**d)]
    return _sp.run(cmd)

def new_session(name, systemd=False):
    """Create a new tmux session.

    If systemd is True then create the new tmux session
    by using 'systemd-run --scope --user'.
    """
    cmd = ['tmux', 'new-session', '-d', '-s', name]
    if systemd:
        systemd_cmd = ['systemd-run', '--scope', '--user']
        systemd_cmd.extend(cmd)
        return _sp.run(systemd_cmd)
    return _sp.run(cmd)

