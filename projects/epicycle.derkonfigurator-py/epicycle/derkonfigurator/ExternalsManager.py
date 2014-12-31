"""
Contains the Externals class 

@author: Dima Potekhin
"""

import os
import shutil

from RepositoryPart import RepositoryPart


class ExternalsManager(RepositoryPart):
    """
    This class manages the external modules
    """

    def __init__(self, reporter, repository_path, external_repositories):
        """
        Constructor
        """
        super(ExternalsManager, self).__init__(reporter, repository_path)
        
        self._config = self.read_yaml("externals_config.yaml")
        
        self._external_repositories = external_repositories
        
        self._scan_external_repositories()
        
    def _scan_external_repositories(self):
        self._available_externals = []
        for external_repository_path in self._external_repositories:
            all_files = [(x, os.path.join(external_repository_path, x)) for x in os.listdir(external_repository_path)]
            dirs = [x for x in all_files if os.path.isdir(x[1])]
            for directory in dirs:
                self._available_externals.append(directory)
        
    def configure(self):
        self.report("Configuring externals")
        
        externals = self._config['externals']
        
        with self.report_sub_level():
            for external in externals:
                self._config_external(external)
            
    def _config_external(self, external):
        external_area, external_name = tuple(external.split(":", 1))
        external_path_dst = self.to_absolute_path(external_area, external_name)
        
        if os.path.exists(external_path_dst):
            return

        self.report("Configuring: " + external)

        with self.report_sub_level():
            
            self.ensure_dir(external_area)
            
            external_path_src = self._locate_external_in_repository(external_name)
            self.report("Repository path: " + external_path_src)
            
            shutil.copytree(external_path_src, external_path_dst)
        
    def _locate_external_in_repository(self, external):
        for directory in self._available_externals:
            if directory[0].lower() == external.lower():
                return directory[1]