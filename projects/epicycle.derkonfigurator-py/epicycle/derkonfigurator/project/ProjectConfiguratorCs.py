__author__ = 'Dima Potekhin'

from ProjectConfigurator import ProjectConfigurator
from epicycle.derkonfigurator.utils import nget


class ProjectConfiguratorCs(ProjectConfigurator):
    def __init__(self, project):
        super(ProjectConfiguratorCs, self).__init__(project)

        self._guid = nget(self.project.config, "guid")

    @property
    def guid(self):
        return self._guid

    def _configure(self):
        self._generate_assemblyinfo()

    def _generate_assemblyinfo(self):
        self.project.report("Generating AssemblyInfo")

        assemblyinfo_template = self.project.environment.resources.subdir("templates", "cs").read_unicode_file("AssemblyInfo.TEMPLATE.cs")

        parameters = {
            'guid': self.guid,
            'version': self.project.repository.version,
            'title': self.project.full_name,
            'description': self.project.description,
            'company': self.project.repository.organization,
            'product': self.project.repository.product,
            'copyright': self.project.repository.copyright,
        }

        self.project.directory.subdir("Properties").write_unicode_file("AssemblyInfo.cs", assemblyinfo_template % parameters)