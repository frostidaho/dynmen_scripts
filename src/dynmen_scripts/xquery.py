from dynmen.rofi import Rofi
from argparse import ArgumentParser as _ArgumentParser

def parse_args(args=None):
    DEFAULT_PROMPT = 'Query: '
    parser = _ArgumentParser(
        description='Display a graphical window' +
        ' with a text entry box. Print the ' +
        'input text to stdout. The menu uses rofi. ',
    )
    parser.add_argument(
        '-p', '--prompt',
        help="Set the prompt text on the left side of the box" +
        ". Defaults to '{}'".format(DEFAULT_PROMPT),
        default=DEFAULT_PROMPT,
        dest='p',
    )
    parser.add_argument(
        '-pw', '--password',
        help="Show *** in entry box",
        action='store_true',
        dest='password',
    )
    parser.add_argument(
        '-f', '--font',
        type=str,
        help='Font to use in menu',
        default='sans 20',
        dest='font',
    )
    d_args = vars(parser.parse_args())
    return d_args

def main(args=None):
    d_args = parse_args(args)
    d_args = {k:v for k,v in d_args.items() if v}
    menu = Rofi(**d_args)
    menu.sync = True
    menu.lines = 1
    res = menu()
    print(res.selected)
    return 0
