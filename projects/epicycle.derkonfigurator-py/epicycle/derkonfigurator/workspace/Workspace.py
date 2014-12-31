__author__ = 'Dima Potekhin'


class Workspace(object):
    def __init__(self, path, reporter):
        self._path = path
        self._reporter = reporter

    @property
    def path(self):
        return self._path
