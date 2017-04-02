from collections import namedtuple as _namedtuple


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
