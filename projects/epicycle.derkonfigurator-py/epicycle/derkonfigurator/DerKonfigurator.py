__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.workspace import Workspace
from Reporter import Reporter


class DerKonfigurator(object):
    def __init__(self, workspace_path):
        self._workspace_path = workspace_path

    @property
    def workspace_path(self): return self._workspace_path

    def run(self):
        reporter = Reporter()

        workspace = Workspace(self.workspace_path, reporter)

        print workspace.path

