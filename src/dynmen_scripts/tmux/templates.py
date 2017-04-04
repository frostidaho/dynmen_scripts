from collections import namedtuple as _namedtuple
FileInfo = _namedtuple('FileInfo', 'name contents executable')
############################################################
# This section is for attaching to a specific session/window/pane.
# tmux_source(...)
############################################################

_tmux_source = """\
#!/usr/bin/sh
tmux source "$PWD/{tmux_commands_file}"
"""
_tmux_commands_attach = '''\
attach -t "{session_id}"
select-window -t "{window_index}"
select-pane -t "{pane_index}"
set -g set-titles on
set -g set-titles-string '#S - dyn-tmux'
setw -g automatic-rename off
'''
_tmux_commands_cd = """\
send-keys -t "{pane_index}" C-z 'cd {directory}' Enter
"""

def _fn_commands_attach(session_id, window_index, pane_index, directory=None, **kw):
    txt = _tmux_commands_attach.format(**locals())
    if directory is not None:
        txt2 = _tmux_commands_cd.format(**locals())
        txt = '\n'.join([txt, txt2])
    return FileInfo('tmux_commands_attach', txt, False)

def tmux_source(**kw):
    tmux_cmds = _fn_commands_attach(**kw)
    txt = _tmux_source.format(tmux_commands_file=tmux_cmds.name)
    return [FileInfo('tmux_source', txt, True), tmux_cmds]

############################################################
# This section is for attaching to the default
# session or spawning one if no sessions exist.
#
# tmux_attach(...)
############################################################ 
_tmux_attach_or_spawn = """\
#!/usr/bin/sh
tmux source "$PWD/{tmux_commands_file}"
retcode=$?
if [ $retcode -ne 0 ]; then
    systemd-run --scope --user tmux new-session\
                -s default\
                -c "{directory}"\
                -d
    tmux source "$PWD/{tmux_commands_file}"
fi
"""

_tmux_commands_attach_default = '''\
attach
set -g set-titles on
set -g set-titles-string '#S - dyn-tmux'
setw -g automatic-rename off
'''

_tmux_commands_cd_default = """\
send-keys C-z 'cd {directory}' Enter
"""

def tmux_attach(directory=None, **kw):
    tmux_commands_file = 'tmux_conf'
    if directory is None:
        directory = '$HOME'
        tmux_conf = _tmux_commands_attach_default
    else:
        tmux_conf = '\n'.join([_tmux_commands_attach_default, _tmux_commands_cd_default])
        tmux_conf = tmux_conf.format(**locals())

    script = _tmux_attach_or_spawn.format(**locals())
    return [
        FileInfo('tmux_attach', script, True),
        FileInfo('tmux_conf', tmux_conf, False),
    ]


