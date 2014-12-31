"""
Contains the Repository class 

@author: Dima Potekhin
"""

import shutil

from ExternalsManager import ExternalsManager
from RepositoryPart import RepositoryPart


class Repository(RepositoryPart):
    """
    This class represents the whole repository that is to be configured
    """

    def __init__(self, reporter, repository_path):
        """
        Constructor
        """
        super(Repository, self).__init__(reporter, repository_path)
        
        self._config = self.read_yaml("repository_config.yaml")
        
    def _init(self):
        self._local_config = self.read_yaml("repository_config.yaml.local")
        
        if not self._local_config:
            self.report("Initializing fresh repository!")
            
            shutil.copy(self.to_absolute_path("repository_config.yaml.local.default"), self.to_absolute_path("repository_config.yaml.local"))
            
            self.report("Please set-up Der Konfigurator by editing repository_config.yaml.local")
            self.report("Rerun after you finished configuring")
            return False
        
        external_repositories = self._local_config['external_repositories']
        
        self.externals_manager = ExternalsManager(self.get_reporter(), self.to_absolute_path("externals"), external_repositories)
        
        return True
        
    def configure(self):
        self.report("Initializing")
        with self.report_sub_level():
            should_continue = self._init()
            if not should_continue:
                return
        
        self.report("Configuring the repository")
        
        with self.report_sub_level():
            self.externals_manager.configure()
            
        self.report("Finished configuring the repository!")