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
