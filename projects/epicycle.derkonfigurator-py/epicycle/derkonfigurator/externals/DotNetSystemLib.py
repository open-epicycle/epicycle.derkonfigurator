__author__ = 'Dima Potekihin'


class DotNetSystemLib(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
