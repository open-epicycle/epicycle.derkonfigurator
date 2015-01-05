"""
Contains the Repository class 

@author: Dima Potekhin
"""

import os
from epicycle.derkonfigurator.utils import nget
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.project.Project import Project


class Repository(WorkspaceEntity):
    CONFIG_FILE_NAME = "repository_config.yaml"
    PROJECTS_DIR = "projects"

    def __init__(self, workspace, path):
        super(Repository, self).__init__(path, workspace.environment, workspace, workspace.reporter)
        
        self._config = self.directory.read_yaml(Repository.CONFIG_FILE_NAME)
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
        for directory in self.directory.subdir(Repository.PROJECTS_DIR).list_subdirs_with_file(Project.CONFIG_FILE_NAME):
            self._projects.append(Project(self, directory.path))

    def _configure_projects(self):
        with self.report_sub_level():
            for project in self._projects:
                project.configure()
