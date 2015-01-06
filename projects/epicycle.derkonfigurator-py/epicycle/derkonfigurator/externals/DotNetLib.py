__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.DirectoryBasedObject import DirectoryBasedObject


class DotNetLib(DirectoryBasedObject):
    def __init__(self, repository, repository_level_subpath, full_name):
        super(DotNetLib, self).__init__(repository.directory.to_full_path(repository_level_subpath))

        self._repository = repository
        self._repository_level_subpath = repository_level_subpath
        self._full_name = full_name

        self._parse_package_name()

    def _parse_package_name(self):
        parts = self._full_name.split('.', 1)

        self._name = parts[0]
        self._version = parts[1]

    @property
    def repository(self):
        return self._repository

    @property
    def repository_level_subpath(self):
        return self._repository_level_subpath

    @property
    def full_name(self):
        return self._full_name

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    def load(self):
        self.repository.report("Loading %s" % self.name)

        # TODO