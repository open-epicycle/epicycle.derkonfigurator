"""
Contains the DirectoryBasedObject class

@author: Dima Potekhin
"""

import os
from utils import read_binary_file, write_binary_file, read_unicode_file, write_unicode_file, read_yaml, ensure_dir


class DirectoryBasedObject(object):
    def __init__(self, path):
        self._path = path
        
    @property
    def path(self):
        return self._path
        
    def to_full_path(self, *sub_path_parts):
        return os.path.join(self._path, *sub_path_parts)

    def read_binary_file(self, *sub_path_parts):
        return read_binary_file(self.to_full_path(*sub_path_parts))

    def write_binary_file(self, sub_path, data):
        return write_binary_file(self.to_full_path(sub_path), data)

    def read_unicode_file(self, *sub_path_parts):
        return read_unicode_file(self.to_full_path(*sub_path_parts))

    def write_unicode_file(self, sub_path, data):
        return write_unicode_file(self.to_full_path(sub_path), data)

    def read_yaml(self, *sub_path_parts):
        return read_yaml(self.to_full_path(*sub_path_parts))

    def ensure_dir(self, *sub_path_parts):
        return ensure_dir(self.to_full_path(*sub_path_parts))
