from collections import namedtuple as _namedtuple

FileInfo = _namedtuple('FileInfo', 'name contents executable')


_tmux_source = """\
#!/usr/bin/sh
tmux source "$PWD/{tmux_commands_file}"
"""
def tmux_source(tmux_commands_file, **kw):
    txt = _tmux_source.format(**locals())
    return FileInfo('tmux_source', txt, True)

_tmux_commands_attach = '''\
attach -t "{session_id}"
select-window -t "{window_index}"
select-pane -t "{pane_index}"
'''
_tmux_commands_cd = """\
send-keys -t "{pane_index}" C-z 'cd {directory}' Enter
"""
def tmux_commands_attach(session_id, window_index, pane_index, directory=None, **kw):
    txt = _tmux_commands_attach.format(**locals())
    if directory is not None:
        txt2 = _tmux_commands_cd.format(**locals())
        txt = '\n'.join([txt, txt2])
    return FileInfo('tmux_commands_attach', txt, False)

_tmux_attach = """\
#!/usr/bin/sh
cd {directory}
tmux attach || systemd-run --scope --user tmux new -s default
"""
def tmux_attach(directory=None, **kw):
    if directory is None:
        directory = '~/'
    txt = _tmux_attach.format(**locals())
    return FileInfo('tmux_attach', txt, True)


