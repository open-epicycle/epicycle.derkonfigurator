__author__ = 'Dima Potekhin'

import os
import re
from epicycle.derkonfigurator.DirectoryBasedObject import DirectoryBasedObject
from epicycle.derkonfigurator.utils import listdir_full, join_ipath


class DotNetLib(DirectoryBasedObject):
    DIGITS_RE = re.compile(r"^\d+$")

    LIB_DIR = "lib"

    def __init__(self, repository, repository_level_subpath, full_name):
        super(DotNetLib, self).__init__(repository.directory.to_full_path(repository_level_subpath))

        self._repository = repository
        self._repository_level_subpath = repository_level_subpath
        self._full_name = full_name

        self._parse_package_name()

        self._libs_by_framework = {}

    def _parse_package_name(self):
        parts = self._full_name.split('.')

        name_parts = []
        version_parts = []

        parts.reverse()
        for part in parts:
            if DotNetLib.DIGITS_RE.match(part) and not name_parts:
                version_parts.append(part)
            else:
                name_parts.append(part)

        name_parts.reverse()
        version_parts.reverse()

        self._name = ".".join(name_parts)
        self._version = ".".join(version_parts)

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
