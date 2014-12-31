__author__ = 'Dima Potekhin'

import shutil
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity


class Workspace(WorkspaceEntity):
    DEFAULT_LOCAL_CONFIG_RESOURCE_ID = "workspace_config.yaml.local.default"
    LOCAL_CONFIG_FILE_NAME = "workspace_config.yaml.local"

    def __init__(self, path, environment, reporter):
        super(Workspace, self).__init__(path, environment, self, reporter)

    def configure(self):
        self.report("Initializing workspace")
        with self.report_sub_level():
            should_continue = self._init()
            if not should_continue:
                return

        self.report("Configuring workspace")

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
