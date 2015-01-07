__author__ = 'Dima Potekhin'


class RepositoryConfigurator(object):
    def __init__(self, repository):
        self._repository = repository

    @property
    def repository(self):
        return self._repository

    def configure(self):
        self._configure()
