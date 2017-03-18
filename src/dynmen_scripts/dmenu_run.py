from dynmen.dmenu import DMenu

def main():
    from os import _exit
    menu = DMenu(
        l=15,
        fn='Dejavu Sans Mono-14',
        case_insensitive=True,
    )
    menu.base_command = ['dmenu_run']
    menu()
    _exit(0)

