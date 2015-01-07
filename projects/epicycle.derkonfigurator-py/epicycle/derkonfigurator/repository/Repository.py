"""
Contains the Repository class 

@author: Dima Potekhin
"""

import os
from epicycle.derkonfigurator.utils import nget
from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity
from epicycle.derkonfigurator.externals.ExternalsManager import ExternalsManager
from epicycle.derkonfigurator.packaging.NuGetPackager import NuGetPackager
from epicycle.derkonfigurator.project.Project import Project
from RepositoryConfiguratorCs import RepositoryConfiguratorCs


class Repository(WorkspaceEntity):
    DEFAULT_VERSION = "0.0.0.0"
    CONFIG_FILE_NAME = "repository_config.yaml"
    EXTERNALS_DIR = "externals"
    PROJECTS_DIR = "projects"

    def __init__(self, workspace, path):
        super(Repository, self).__init__(path, workspace.environment, workspace, workspace.reporter)
        
        self._config = self.directory.read_yaml(Repository.CONFIG_FILE_NAME)
        self._full_name = os.path.split(path)[1]

        self._parse_full_name()

        version_data = self.directory.read_unicode_file("version")
        self._version = version_data.strip() if version_data else Repository.DEFAULT_VERSION
        self._organization = nget(self._config, "organization", default="")
        self._product = nget(self._config, "product", default=self.full_name)
        self._copyright = nget(self._config, "copyright", default="")
        self._title = nget(self._config, "title", default="")
        self._license_url = nget(self._config, "license_url", default="")
        self._url = nget(self._config, "url", default="")
        self._description = nget(self._config, "description", default="")
        self._summary = nget(self._config, "summary", default="")
        self._release_notes = nget(self._config, "release_notes", default="")
        self._tags = nget(self._config, "tags", default="")

        self._source_infocomment = self.directory.read_unicode_file("comment")

        self._externals = ExternalsManager(self, Repository.EXTERNALS_DIR)
        self._projects = []

        self._configurator = self._create_configurator()
        self._nuget_packager = NuGetPackager(self)

    def _parse_full_name(self):
        parts = self.full_name.split("-", 1)

        self._name = parts[0]
        self._kind = parts[0].lower()

    def _create_configurator(self):
        # Currently assuming a .NET configurator
        return RepositoryConfiguratorCs(self)

    @property
    def config(self):
        return self._config

    @property
    def configurator(self):
        return self._configurator

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
    def version(self):
        return self._version

    @property
    def organization(self):
        return self._organization

    @property
    def product(self):
        return self._product

    @property
    def copyright(self):
        return self._copyright

    @property
    def title(self):
        return self._title

    @property
    def license_url(self):
        return self._license_url

    @property
    def url(self):
        return self._url

    @property
    def description(self):
        return self._description

    @property
    def summary(self):
        return self._summary

    @property
    def release_notes(self):
        return self._release_notes

    @property
    def tags(self):
        return self._tags

    @property
    def source_infocomment(self):
        return self._source_infocomment

    @property
    def externals(self):
        return self._externals

    @property
    def projects(self):
        return self._projects

    def get_project(self, full_name):
        for project in self.projects:
            if project.full_name.lower() == full_name.lower():
                return project

        return None

    def configure(self):
        self.report("Configuring the repository %s" % self.full_name)

        with self.report_sub_level():
            self._load_externals()
            self._load_projects()
            self._resolve_project_references()
            self._flatten_dependencies()
            self._configure_projects()
            self.configurator.configure()
            self._configure_packagers()

    def _load_externals(self):
        self._externals.load()

    def _load_projects(self):
        to_repository_relative_path = "../.."

        self.report("Loading projects")

        with self.report_sub_level():
            for directory in self.directory.subdir(Repository.PROJECTS_DIR).list_subdirs_with_file(Project.CONFIG_FILE_NAME):
                self._projects.append(Project(self, directory.path, to_repository_relative_path))
            self.report("Loaded %d projects" % len(self._projects))

    def _resolve_project_references(self):
        self.report("Resolving project references")
        for project in self._projects:
            project.resolve_dependencies()

    def _flatten_dependencies(self):
        self.report("Flattening dependencies")
        for project in self._projects:
            project.flatten_dependencies()

    def _configure_projects(self):
        if not self._projects:
            self.report("No projects to configure!")
            return

        self.report("Configuring projects")
        with self.report_sub_level():
            for project in self._projects:
                project.configure()

    def _configure_packagers(self):
        self.report("Configuring packagers")

        with self.report_sub_level():
            self._nuget_packager.configure()
