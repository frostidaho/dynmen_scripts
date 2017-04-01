import os
import stat
from collections import namedtuple, OrderedDict
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from itertools import chain

FileInfo = namedtuple('FileInfo', 'name contents executable')

@contextmanager
def scripts(main_file, *files):
    S_IEXEC = stat.S_IEXEC
    files = main_file, *files
    d = OrderedDict()
    path_join = os.path.join
    with TemporaryDirectory() as td:
        for file_info in chain([main_file], files):
            path = path_join(td, file_info.name)
            with open(path, mode='w') as fobj:
                fobj.write(file_info.contents)
            if file_info.executable:
                st = os.stat(path)
                os.chmod(path, st.st_mode | S_IEXEC)
        yield td, main_file.name

