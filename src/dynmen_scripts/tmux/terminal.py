def xfce4(script_path):
    cmd = [
        'xfce4-terminal',
        '--show-borders',
        '--maximize',
        '--command={}'.format(script_path),
    ]
    return cmd

def alacritty(script_path):
    return ['alacritty', '-e', script_path]


