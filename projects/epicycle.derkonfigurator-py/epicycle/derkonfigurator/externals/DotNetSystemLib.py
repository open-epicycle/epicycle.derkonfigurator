__author__ = 'Dima Potekihin'


class DotNetSystemLib(object):
    def __init__(self, name, framework):
        self._name = name
        self._framework = framework

    @property
    def name(self):
        return self._name

    @property
    def framework(self):
        return self._framework
