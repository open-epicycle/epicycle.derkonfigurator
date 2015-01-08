__author__ = 'Dima Potekhin'

import os
from epicycle.derkonfigurator.DirectoryBasedObject import DirectoryBasedObject
from epicycle.derkonfigurator.utils import listdir_full, join_ipath, parse_versioned_name


class DotNetLib(DirectoryBasedObject):
    LIB_DIR = "lib"

    def __init__(self, repository, repository_level_subpath, full_name, is_auto):
        super(DotNetLib, self).__init__(repository.directory.to_full_path(repository_level_subpath))

        self._repository = repository
        self._repository_level_subpath = repository_level_subpath
        self._full_name = full_name
        self._is_auto = is_auto
        self._name, self._version = parse_versioned_name(self._full_name)

        self._libs_by_framework = {}

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
    def is_auto(self):
        return self._is_auto

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def available_frameworks(self):
        return self._libs_by_framework.keys()

    def get_libs(self, framework):
        return self._libs_by_framework[framework.lower()]

    def load(self):
        self.repository.report("Loading %s" % self.name)

        self._collect_libs()

    def _collect_libs(self):
        repository_level_subpath = join_ipath(self.repository_level_subpath, DotNetLib.LIB_DIR)

        global_libs = self._collect_framework_libs(repository_level_subpath)

        self._libs_by_framework[""] = global_libs
        for item, item_path in listdir_full(self.repository.directory.to_full_path(repository_level_subpath)):
            if os.path.isdir(item_path):
                libs = self._collect_framework_libs(join_ipath(repository_level_subpath, item))
                self._libs_by_framework[item.lower()] = global_libs + libs

    def _collect_framework_libs(self, repository_level_subpath):
        lib_files = []
        for item, item_path in listdir_full(self.repository.directory.to_full_path(repository_level_subpath)):
            if os.path.isfile(item_path):
                lib_files.append(join_ipath(repository_level_subpath, item))

        return lib_files
