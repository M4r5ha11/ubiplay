# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

import mimetypes
import os

from collections import namedtuple


import settings
ROOT_DIR = os.path.abspath(settings.ROOT_DIR)


MIMETYPE_DIR = "inode/directory"
MIMETYPE_DEFAULT = "application/octet-stream"


Entry = namedtuple("Entry", ["mimetype", "name", "path"])

def create_entry(filepath):
    name = os.path.basename(filepath)
    full = os.path.join(ROOT_DIR, filepath)
    if os.path.isdir(full):
        mimetype = MIMETYPE_DIR
    else:
        mimetype = mimetypes.guess_type(full)[0]
        if mimetype is None:
            mimetype = MIMETYPE_DEFAULT
    return Entry(mimetype=mimetype, name=name, path=filepath)


class DirContent(object):
    def __init__(self, dirpath, fulldirpath):
        self._path = dirpath
        self._dirs = []
        self._files = []
        for name in sorted(os.listdir(fulldirpath)):
            if name[0] == ".":
                continue
            entry = create_entry(os.path.join(dirpath, name))
            if entry.mimetype == MIMETYPE_DIR:
                self._dirs.append(entry)
            else:
                self._files.append(entry)

    @property
    def path(self):
        return self._path

    @property
    def dirs(self):
        return self._dirs

    @property
    def files(self):
        return self._files

class FileContent(object):
    def __init__(self, path):
        self._entry = create_entry(path)

    @property
    def entry(self):
        return self._entry


def get_content(filepath):
    fullpath = os.path.join(ROOT_DIR, filepath)
    if not os.path.exists(fullpath):
        return None

    if os.path.isdir(fullpath):
        return DirContent(filepath, fullpath)
    else:
        return FileContent(filepath)


def get_parent_filepath(filepath):
    if filepath == "":
        return None
    return os.path.dirname(filepath)


def get_raw(filepath):
    fullpath = os.path.join(ROOT_DIR, filepath)
    mimetype = mimetypes.guess_type(fullpath)[0]
    return open(fullpath).read(), mimetype
