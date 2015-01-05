"""
Contains the DirectoryBasedObject class

@author: Dima Potekhin
"""

from Directory import Directory


class DirectoryBasedObject(object):
    def __init__(self, path):
        self._directory = Directory(path)

    @property
    def directory(self):
        return self._directory

    @property
    def path(self):
        return self._directory.path
