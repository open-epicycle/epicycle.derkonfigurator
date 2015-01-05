__author__ = 'Dima Potekhin'

import os
import re
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.utils import nget
from ProjectConfiguratorCs import ProjectConfiguratorCs


class Project(WorkspaceEntity):
    CONFIG_FILE_NAME = "project_config.yaml"
    _FULL_NAME_PARSING_RE = re.compile("^([^_]+)_(.+)$")

    def __init__(self, repository, path):
        super(Project, self).__init__(path, repository.environment, repository.workspace, repository.reporter)

        self._repository = repository

        self._config = self.directory.read_yaml(Project.CONFIG_FILE_NAME)
        self._full_name = os.path.split(path)[1]

        self._type = 'lib'
        self._parse_full_name()

        config_type = nget(self._config, 'type')
        if config_type:
            self._type = config_type

        self._description = nget(self.config, "description", "")

        self._pretty_label = "%s (%s/%s)" % (self.name, self.kind, self.type)

        self._configurator = self._create_configurator()

    def _parse_full_name(self):
        name, serialized_kind = Project._FULL_NAME_PARSING_RE.match(self.full_name).groups()

        serialized_kind_parts = serialized_kind.lower().split('-')

        self._name = name
        self._kind = serialized_kind_parts[0]

        if len(serialized_kind_parts) == 2 and serialized_kind_parts[1] == 'test':
            self._type = 'test'

    def _create_configurator(self):
        if self.kind == 'cs':
            return ProjectConfiguratorCs(self)

    @property
    def repository(self):
        return self._repository

    @property
    def full_name(self):
        return self._full_name

    @property
    def name(self):
        return self._name

    @property
    def kind(self):
        return self._kind

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def pretty_label(self):
        return self._pretty_label

    def configure(self):
        self.report("Configuring the project %s" % self.pretty_label)

        with self.report_sub_level():
            self._configurator.configure()
