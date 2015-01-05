__author__ = 'Dima Potekhin'

from Directory import Directory


class Environment(object):
    def __init__(self, resources_path):
        self._resources = Directory(resources_path)

    @property
    def resources(self):
        return self._resources