tmux_source = """
#!/usr/bin/sh
tmux source "$PWD/{tmux_file}"
"""

tmux_commands_attach = '''
attach -t "{session_id}"
select-window -t "{window_index}"
select-pane -t {pane_index}
'''

tmux_attach = """
#!/usr/bin/sh
cd ~/
tmux attach || systemd-run --scope --user tmux new -s default
"""
