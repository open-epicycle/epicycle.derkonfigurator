"""
Contains the Repository class 

@author: Dima Potekhin
"""

import os
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.project.Project import Project

class Repository(WorkspaceEntity):
    CONFIG_FILE_NAME = "repository_config.yaml"
    PROJECTS_DIR = "projects"

    def __init__(self, parent, path):
        super(Repository, self).__init__(path, parent.environment, parent.workspace, parent.reporter)
        
        self._config = self.read_yaml("repository_config.yaml")
        self._name = os.path.split(path)[1]

        self._projects = []

    @property
    def name(self):
        return self._name

    def configure(self):
        self.report("Configuring the repository %s" % self.name)

        with self.report_sub_level():
            self._load_projects()
            self._configure_projects()

    def _load_projects(self):
        for item, full_path in self.listdir_dirs_with_file_full(Project.CONFIG_FILE_NAME, self.PROJECTS_DIR):
            self._projects.append(Project(self.workspace, full_path))

    def _configure_projects(self):
        with self.report_sub_level():
            for project in self._projects:
                project.configure()
