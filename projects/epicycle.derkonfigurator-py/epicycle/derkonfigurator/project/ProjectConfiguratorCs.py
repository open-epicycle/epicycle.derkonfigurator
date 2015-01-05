__author__ = 'Dima Potekhin'

from ProjectConfigurator import ProjectConfigurator
from epicycle.derkonfigurator.utils import nget


class ProjectConfiguratorCs(ProjectConfigurator):
    def __init__(self, project):
        super(ProjectConfiguratorCs, self).__init__(project)

        self._source_files = []

        self._guid = nget(self.project.config, "guid")

    @property
    def guid(self):
        return self._guid

    @property
    def source_files(self):
        return self._source_files

    def _configure(self):
        self._find_source_files()
        self._generate_assemblyinfo()

    def _find_source_files(self):
        self._source_files = self.project.directory.find_files_rec(extension=".cs", ignore_dirs=['obj', 'bin'])
        self.project.report("Found %d source files" % len(self.source_files))

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
