__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.utils import nget
from RepositoryConfigurator import RepositoryConfigurator


class RepositoryConfiguratorCs(RepositoryConfigurator):
    def __init__(self, repository):
        super(RepositoryConfiguratorCs, self).__init__(repository)

        self._supported_frameworks = nget(self.repository.config, "dotnet_frameworks", [])

    @property
    def supported_frameworks(self):
        return self._supported_frameworks

    def _configure(self):
        self.repository.report("Configuring .NET repository")
