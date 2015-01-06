__author__ = 'Dima Potekhin'


class ProjectConfigurator(object):
    def __init__(self, project):
        self._project = project

    @property
    def project(self):
        return self._project

    def flatten_dependencies(self):
        self._flatten_dependencies()

    def configure(self):
        self._configure()
