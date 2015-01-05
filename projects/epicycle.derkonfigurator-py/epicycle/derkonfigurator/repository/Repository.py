"""
Contains the Repository class 

@author: Dima Potekhin
"""

import os

from ExternalsManager import ExternalsManager
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.utils import nget

class Repository(WorkspaceEntity):
    CONFIG_FILE_NAME = "repository_config.yaml"

    def __init__(self, parent, path):
        super(Repository, self).__init__(path, parent.environment, parent.workspace, parent.reporter)
        
        self._config = self.read_yaml("repository_config.yaml")
        self._name = os.path.split(path)[1]

    @property
    def name(self):
        return self._name

    def configure(self):
        self.report("Configuring the repository %s" % self.name)

        print self._config

        with self.report_sub_level():
            self.report("Finished configuring the repository!")

        return True