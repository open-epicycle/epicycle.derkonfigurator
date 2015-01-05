__author__ = 'Dima Potekhin'

import os
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity


class Project(WorkspaceEntity):
    CONFIG_FILE_NAME = "project_config.yaml"

    def __init__(self, parent, path):
        super(Project, self).__init__(path, parent.environment, parent.workspace, parent.reporter)

        self._config = self.directory.read_yaml(Project.CONFIG_FILE_NAME)
        self._name = os.path.split(path)[1]

    @property
    def name(self):
        return self._name

    def configure(self):
        self.report("Configuring the project %s" % self.name)

        # TODO-
