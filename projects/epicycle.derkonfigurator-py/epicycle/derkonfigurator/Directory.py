__author__ = 'Dima Potekhin'

import os
from utils import read_binary_file, write_binary_file, read_unicode_file, write_unicode_file, read_yaml, ensure_dir, listdir_full


class Directory(object):
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    def to_full_path(self, *subpath_parts):
        return os.path.join(self._path, *subpath_parts)

    def subdir(self, *subpath_parts):
        return Directory(self.to_full_path(*subpath_parts))

    def ensure_subdir(self, *subpath_parts):
        full_path = self.to_full_path(*subpath_parts)
        ensure_dir(full_path)

        return Directory(full_path)

    def list_subdirs(self):
        return [Directory(full_path)
                for item, full_path
                in listdir_full(self.path)
                if os.path.isdir(full_path)]

    def list_subdirs_with_file(self, file_subpath):
        return [directory for directory in self.list_subdirs() if directory.contains_file(file_subpath)]

    def contains_file(self, file_subpath):
        return os.path.isfile(self.to_full_path(file_subpath))

    def contains_subdir(self, file_subpath):
        return os.path.isdir(self.to_full_path(file_subpath))

    def read_binary_file(self, file_subpath):
        return read_binary_file(self.to_full_path(file_subpath))

    def write_binary_file(self, file_subpath, data):
        return write_binary_file(self.to_full_path(file_subpath), data)

    def read_unicode_file(self, file_subpath):
        return read_unicode_file(self.to_full_path(file_subpath))

    def write_unicode_file(self, file_subpath, data):
        return write_unicode_file(self.to_full_path(file_subpath), data)

    def read_yaml(self, file_subpath):
        return read_yaml(self.to_full_path(file_subpath))
