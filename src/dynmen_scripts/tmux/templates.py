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
def tmux_commands_attach(session_id, window_index, pane_index, **kw):
    txt = _tmux_commands_attach.format(**locals())
    return FileInfo('tmux_commands_attach', txt, False)

_tmux_attach = """
#!/usr/bin/sh
cd ~/
tmux attach || systemd-run --scope --user tmux new -s default
"""
def tmux_attach(**kw):
    txt = _tmux_attach
    return FileInfo('tmux_attach', txt, True)

    
