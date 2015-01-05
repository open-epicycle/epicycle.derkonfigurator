__author__ = 'Dima Potekhin'

import os
import shutil
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.repository import Repository


class Workspace(WorkspaceEntity):
    DEFAULT_LOCAL_CONFIG_RESOURCE_ID = "workspace_config.yaml.local.default"
    LOCAL_CONFIG_FILE_NAME = "workspace_config.yaml.local"

    def __init__(self, path, environment, reporter):
        super(Workspace, self).__init__(path, environment, self, reporter)

        self._repositories = []

    def configure(self):
        self.report("Initializing workspace")
        with self.report_sub_level():
            should_continue = self._init()
            if not should_continue:
                return

        self.report("Configuring workspace")
        self._load_repositories()
        self._configure_repositories()

    def _init(self):
        self._local_config = self.read_yaml(Workspace.LOCAL_CONFIG_FILE_NAME)

        if not self._local_config:
            self.report("Initializing a fresh workspace!")

            template_path = self.environment.resources.resource_path(Workspace.DEFAULT_LOCAL_CONFIG_RESOURCE_ID)
            shutil.copy(template_path, self.to_full_path(Workspace.LOCAL_CONFIG_FILE_NAME))

            self.report("Please set-up Der Konfigurator by editing %s" % Workspace.LOCAL_CONFIG_FILE_NAME)
            self.report("Rerun after you finished configuring")
            return False
        else:
            self.report("Workspace already initialized")

            self._external_repositories_path = self._local_config['external_repositories']

            return True

    def _load_repositories(self):
        for directory in os.listdir(self.path):
            full_path = os.path.join(self.path, directory)
            self._process_potential_repository(full_path)

    def _process_potential_repository(self, path):
        if not os.path.isdir(path):
            return

        if not os.path.isfile(os.path.join(path, Repository.CONFIG_FILE_NAME)):
            return

        repository = Repository(self, path)
        self._repositories.append(repository)

    def _configure_repositories(self):
        with self.report_sub_level():
            for repository in self._repositories:
                repository.configure()