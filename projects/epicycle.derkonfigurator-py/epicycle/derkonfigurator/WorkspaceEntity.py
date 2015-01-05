__author__ = 'Dima Potekhin'

from DirectoryBasedObject import DirectoryBasedObject


class WorkspaceEntity(DirectoryBasedObject):
    def __init__(self, path, environment, workspace, reporter):
        super(WorkspaceEntity, self).__init__(path)

        self._environment = environment
        self._workspace = workspace
        self._reporter = reporter

    @property
    def environment(self):
        return self._environment

    @property
    def workspace(self):
        return self._workspace

    @property
    def reporter(self):
        return self._reporter

    def report(self, text):
        self._reporter.report(text)

    def report_sub_level(self):
        return self._reporter.sub_level()