__author__ = 'Dima Potekhin'

from RepositoryConfigurator import RepositoryConfigurator


class RepositoryConfiguratorCs(RepositoryConfigurator):
    def __init__(self, project):
        super(RepositoryConfiguratorCs, self).__init__(project)

    def _configure(self):
        self.repository.report("Configuring .NET repository")
        pass