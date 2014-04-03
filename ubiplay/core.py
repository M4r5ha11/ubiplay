# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

import mimetypes
import os

from collections import namedtuple


import settings
ROOT_DIR = os.path.abspath(settings.ROOT_DIR)


def create_entry(filepath):
    name = os.path.basename(filepath)
    full = os.path.join(ROOT_DIR, filepath)
    if os.path.isdir(full):
        mimetype = MIMETYPE_DIR
    else:
        mimetype = mimetypes.guess_type(full)[0]
    return Entry(mimetype=mimetype, name=name, path=filepath)


MIMETYPE_DIR = "inode/directory"


Entry = namedtuple("Entry", ["mimetype", "name", "path"])


class DirContent(object):

    def __init__(self, dirpath, fulldirpath):
        self._lst = [create_entry(os.path.join(dirpath, x)) for x in sorted(os.listdir(fulldirpath)) if x[0] != "."]

    def __getitem__(self, x):
        return self._lst[x]


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
