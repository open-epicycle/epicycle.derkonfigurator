__author__ = 'Dima Potekhin'

import shutil
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.repository import Repository


class Workspace(WorkspaceEntity):
    DEFAULT_LOCAL_CONFIG_RESOURCE_NAME = "workspace_config.yaml.local.default"
    LOCAL_CONFIG_FILE_NAME = "workspace_config.yaml.local"

    def __init__(self, path, environment, reporter):
        super(Workspace, self).__init__(path, environment, self, reporter)

        self._repositories = []

    def configure(self):
        self.report("Configuring the workspace")
        with self.report_sub_level():
            should_continue = self._init()
            if not should_continue:
                return

            self._load_repositories()
            self._configure_repositories()

    def _init(self):
        self._local_config = self.directory.read_yaml(Workspace.LOCAL_CONFIG_FILE_NAME)

        if not self._local_config:
            self.report("Initializing a fresh workspace!")

            template_path = self.environment.resources.to_full_path(Workspace.DEFAULT_LOCAL_CONFIG_RESOURCE_NAME)
            shutil.copy(template_path, self.directory.to_full_path(Workspace.LOCAL_CONFIG_FILE_NAME))

            self.report("Please set-up Der Konfigurator by editing %s" % Workspace.LOCAL_CONFIG_FILE_NAME)
            self.report("Rerun after you finished configuring")
            return False
        else:
            self._external_repositories_path = self._local_config['external_repositories']

            return True

    def _load_repositories(self):
        for directory in self.directory.list_subdirs_with_file(Repository.CONFIG_FILE_NAME):
            self._repositories.append(Repository(self.workspace, directory.path))

    def _configure_repositories(self):
        for repository in self._repositories:
            repository.configure()
