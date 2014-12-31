__author__ = 'Dima Potekhin'


class Environment(object):
    def __init__(self, resources):
        self._resources = resources

    @property
    def resources(self):
        return self._resources