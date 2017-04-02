"""
common.py contains some data structures and constants
"""
from collections import namedtuple as _namedtuple
from os.path import expanduser as _expanduser
from weakref import WeakSet as _WeakSet
from weakref import WeakValueDictionary as _WeakValueDictionary

PaneInfo = _namedtuple(
    'PaneInfo',
    (
        'session_id',
        'window_index',
        'pane_index',
        'pane_current_path',
        'pane_current_command',
        'session_name',
        'pane_title',
        'window_name',
    ),
)

NO_PANE = PaneInfo._make((None for i in range(len(PaneInfo._fields))))

FileInfo = _namedtuple('FileInfo', 'name contents executable')
HOME_DIR = _expanduser('~')


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
