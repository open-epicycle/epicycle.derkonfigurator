__author__ = 'Dima Potekhin'

from ProjectConfigurator import ProjectConfigurator
from epicycle.derkonfigurator.utils import nget


class ProjectConfiguratorCs(ProjectConfigurator):
    _SOURCE_INFOCOMMENT_INSERTOID_ID = "INFO"

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
        self._generate_source_infocomments()

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

    def _generate_source_infocomments(self):
        infocomment = self._generate_infocomment()

        insertoid_name = ProjectConfiguratorCs._SOURCE_INFOCOMMENT_INSERTOID_ID

        for source_file in self._source_files:
            if not self.project.has_insertoid(source_file, insertoid_name):
                self.project.report("WARNING: No %s insertoid in %s" % (insertoid_name, source_file))

            self.project.write_insertoid(source_file, insertoid_name, infocomment)

    def _generate_infocomment(self):
        raw_comment = self.project.repository.source_infocomment

        if not raw_comment:
            return ""

        lines = raw_comment.split("\n")
        return "\n%s\n// " % "\n".join(["// " + x for x in lines])
