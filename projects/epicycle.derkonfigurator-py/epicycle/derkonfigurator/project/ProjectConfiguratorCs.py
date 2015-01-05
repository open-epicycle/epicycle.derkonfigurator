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

        self.project.write_template(
            "Properties/AssemblyInfo.cs", "templates/cs/AssemblyInfo.TEMPLATE.cs",
            guid=self.guid,
            version=self.project.repository.version,
            title=self.project.full_name,
            description=self.project.description,
            company=self.project.repository.organization,
            product=self.project.repository.product,
            copyright=self.project.repository.copyright,
        )
