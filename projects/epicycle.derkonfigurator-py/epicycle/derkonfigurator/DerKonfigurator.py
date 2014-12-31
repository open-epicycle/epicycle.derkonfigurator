import os

__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.workspace import Workspace
from Reporter import Reporter
from Resources import Resources


class DerKonfigurator(object):
    def __init__(self, derkonfigurator_path, workspace_path):
        self._derkonfigurator_path = derkonfigurator_path
        self._workspace_path = workspace_path

        self._resources = Resources(os.path.join(derkonfigurator_path, "resources"))

    @property
    def derkonfigurator_path(self):
        return self._derkonfigurator_path

    @property
    def workspace_path(self):
        return self._workspace_path

    @property
    def resources(self):
        return self._resources

    def run(self):
        reporter = Reporter()

        workspace = Workspace(self.workspace_path, reporter)
