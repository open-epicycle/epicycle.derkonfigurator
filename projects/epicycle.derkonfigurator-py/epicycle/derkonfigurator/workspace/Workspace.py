__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.WorkspaceEntity import WorkspaceEntity


class Workspace(WorkspaceEntity):
    def __init__(self, path, environment, reporter):
        super(Workspace, self).__init__(path, environment, self, reporter)
