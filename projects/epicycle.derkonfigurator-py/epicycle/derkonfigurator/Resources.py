__author__ = 'Dima Potekhin'

import os


class Resources(object):
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    def resource_path(self, resource_id):
        return os.path.join(self.path, resource_id)
