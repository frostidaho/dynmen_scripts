from weakref import WeakValueDictionary as _WeakValueDictionary
from weakref import WeakSet as _WeakSet

class Register:
    def __new__(cls, *args, **kwargs):
        instance = object.__new__(cls)
        if "_instances" not in cls.__dict__:
            cls._instances = _WeakSet()
        cls._instances.add(instance)
        return instance

    def __init__(self, name):
        self.name = name
        self.registered = _WeakValueDictionary()
        self.default = None

    def __getitem__(self, key):
        return self.registered[key]

    def __call__(self, fn, name='', default=False):
        if not name:
            name = fn.__name__
        if self.default is None:
            self.default = name
        elif default:
            self.default = name
        self.registered[name] = fn
        return fn

    def __repr__(self):
        cname = self.__class__.__name__
        name = self.name
        dflt = self.default
        return '<{cname}({name!r}): default -> {dflt}>'.format(**locals())


register_terminal = Register('terminal')


@register_terminal
def xfce4(script_path):
    cmd = [
        'xfce4-terminal',
        '--show-borders',
        '--maximize',
        '--command={}'.format(script_path),
    ]
    return cmd

@register_terminal
def alacritty(script_path):
    return ['alacritty', '-e', script_path]


class Attach:
    register_terminal = register_terminal
    def __init__(self, backend=''):
        rt = self.register_terminal
        if backend:
            self.backend = rt[backend]
        else:
            self.backend = rt[rt.default]

    def __call__(self):
        pass
