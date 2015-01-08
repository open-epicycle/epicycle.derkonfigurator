__author__ = 'Dima Potekhin'

import os
from epicycle.derkonfigurator.DirectoryBasedObject import DirectoryBasedObject
from epicycle.derkonfigurator.utils import listdir_full, join_ipath
from DotNetLib import DotNetLib
from DotNetSystemLib import DotNetSystemLib


class ExternalsManager(DirectoryBasedObject):
    NUGET_DIR = "NuGet"
    DOT_NET_LIB_DIR = "lib_dotnet"

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

        self._add_system_libs()

        with self.repository.report_sub_level():
            self._load_libs(ExternalsManager.DOT_NET_LIB_DIR, False)
            self._load_libs(ExternalsManager.NUGET_DIR, True)

    def _add_system_libs(self):
        system_lib_names = [
            "System.Numerics",
            "System.Drawing",
        ]

        for system_lib_name in system_lib_names:
            self._add_lib(DotNetSystemLib(system_lib_name))

    def _load_libs(self, externals_level_subpath, is_auto):
        directory = self.directory.subdir(externals_level_subpath)

        if not os.path.isdir(directory.path):
            return

        for item, item_path in listdir_full(directory.path):
            if os.path.isdir(item_path):
                self._load_potential_dotnet_lib(item, join_ipath(externals_level_subpath, item), is_auto)

    def _load_potential_dotnet_lib(self, full_name, externals_level_subpath, is_auto):
        lib_repository_level_subpath = join_ipath(self.repository_level_subpath, externals_level_subpath)

        lib = DotNetLib(self.repository, lib_repository_level_subpath, full_name, is_auto)
        lib.load()

        self._add_lib(lib)

    def _add_lib(self, lib):
        self._dotnet_libs[lib.name.lower()] = lib
