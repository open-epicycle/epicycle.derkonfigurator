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
        self._load_dotnet_lib_config()

        self._dotnet_libs = {}

    def _load_dotnet_lib_config(self):
        config = self.repository.workspace.environment.resources.read_yaml("dotnet_lib_config.yaml")

        self._dotnet_lib_config = {}

        for lib in config['libs']:
            self._dotnet_lib_config[lib['name']] = lib

    @property
    def repository(self):
        return self._repository

    @property
    def repository_level_subpath(self):
        return self._repository_level_subpath

    @property
    def available_dotnet_libs(self):
        return [x.name for x in self._dotnet_libs]

    def get_dotnet_lib(self, framework, lib):
        key = lib.lower()
        return self._dotnet_libs[framework][key] if key in self._dotnet_libs[framework] else None

    def load(self):
        for framework in self.repository.configurator.supported_frameworks:
            self._load_framework(framework)

    def _load_framework(self, framework):
        self.repository.report("Loading externals (%s)" % framework)

        with self.repository.report_sub_level():
            self._add_system_libs(framework)
            self._load_libs(ExternalsManager.DOT_NET_LIB_DIR, framework, False)
            self._load_libs(ExternalsManager.NUGET_DIR, framework, True)

    def _add_system_libs(self, framework):
        system_lib_names = [
            "System.Drawing",
        ]

        if framework != 'net35':
            system_lib_names.append("System.Numerics")

        if framework != 'net40':
            system_lib_names.append("System.Threading")

        for system_lib_name in system_lib_names:
            self._add_lib(framework, DotNetSystemLib(system_lib_name, framework))

    def _load_libs(self, externals_level_subpath, framework, is_auto):
        directory = self.directory.subdir(externals_level_subpath)

        if not os.path.isdir(directory.path):
            return

        for item, item_path in listdir_full(directory.path):
            if os.path.isdir(item_path):
                self._load_potential_dotnet_lib(item, join_ipath(externals_level_subpath, item), framework, is_auto)

    def _load_potential_dotnet_lib(self, full_name, externals_level_subpath, framework, is_auto):
        lib_repository_level_subpath = join_ipath(self.repository_level_subpath, externals_level_subpath)

        lib = DotNetLib(self.repository, lib_repository_level_subpath, full_name, framework, is_auto)
        if lib.name in self._dotnet_lib_config and framework not in self._dotnet_lib_config[lib.name]['frameworks']:
            return

        lib.load()

        self._add_lib(framework, lib)

    def _add_lib(self, framework, lib):
        if not framework in self._dotnet_libs:
            self._dotnet_libs[framework] = {}

        self._dotnet_libs[framework][lib.name.lower()] = lib
