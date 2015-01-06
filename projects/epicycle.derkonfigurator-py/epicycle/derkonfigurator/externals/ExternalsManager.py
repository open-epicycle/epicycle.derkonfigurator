__author__ = 'Dima Potekhin'

import os
from epicycle.derkonfigurator.DirectoryBasedObject import DirectoryBasedObject
from epicycle.derkonfigurator.utils import listdir_full, join_ipath
from DotNetLib import DotNetLib


class ExternalsManager(DirectoryBasedObject):
    NUGET_DIR = "NuGet"

    def __init__(self, repository, repository_level_subpath):
        super(ExternalsManager, self).__init__(repository.directory.to_full_path(repository_level_subpath))

        self._repository = repository
        self._repository_level_subpath = repository_level_subpath

        self._dotnet_libs = {}

    @property
    def repository(self):
        return self._repository

    @property
    def repository_level_subpath(self):
        return self._repository_level_subpath

    @property
    def available_dotnet_libs(self):
        return [x.name for x in self._dotnet_libs]

    def get_dotnet_lib(self, name):
        return self._dotnet_libs[name.lower()]

    def load(self):
        self.repository.report("Loading externals")

        with self.repository.report_sub_level():
            self._load_nuget(ExternalsManager.NUGET_DIR)

    def _load_nuget(self, externals_level_subpath):
        self.repository.report("Loading NuGet packages")

        with self.repository.report_sub_level():
            directory = self.directory.subdir(externals_level_subpath)

            for item, item_path in listdir_full(directory.path):
                if os.path.isdir(item_path):
                    self._load_potential_dotnet_lib(item, join_ipath(externals_level_subpath, item))

    def _load_potential_dotnet_lib(self, full_name, externals_level_subpath):
        lib_repository_level_subpath = join_ipath(self.repository_level_subpath, externals_level_subpath)

        lib = DotNetLib(self.repository, lib_repository_level_subpath, full_name)
        lib.load()

        self._dotnet_libs[lib.name.lower()] = lib
