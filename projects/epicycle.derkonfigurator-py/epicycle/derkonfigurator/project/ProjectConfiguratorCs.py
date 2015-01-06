__author__ = 'Dima Potekhin'

from ProjectConfigurator import ProjectConfigurator
from epicycle.derkonfigurator.utils import nget, split_into_lines


class ProjectConfiguratorCs(ProjectConfigurator):
    _SOURCE_INFOCOMMENT_INSERTOID_ID = "INFO"

    def __init__(self, project):
        super(ProjectConfiguratorCs, self).__init__(project)

        self._source_files = []

        self._project_guid = nget(self.project.config, "project_guid")
        self._assemblyinfo_guid = nget(self.project.config, "assemblyinfo_guid")

    @property
    def project_guid(self):
        return self._project_guid

    @property
    def assemblyinfo_guid(self):
        return self._assemblyinfo_guid

    @property
    def source_files(self):
        return self._source_files

    def _configure(self):
        self._find_source_files()
        self._generate_assemblyinfo()
        self._generate_source_infocomments()
        self._generate_vs_project_file()

    def _find_source_files(self):
        self._source_files = self.project.directory.find_files_rec(extension=".cs", ignore_dirs=['obj', 'bin'])
        self.project.report("Found %d source files" % len(self.source_files))

    def _generate_assemblyinfo(self):
        self.project.report("Generating AssemblyInfo")

        self.project.write_template(
            "Properties/AssemblyInfo.cs", "templates/cs/AssemblyInfo.TEMPLATE.cs",
            guid=self.assemblyinfo_guid,
            version=self.project.repository.version,
            title=self.project.full_name,
            description=self.project.description,
            company=self.project.repository.organization,
            product=self.project.repository.product,
            copyright=self.project.repository.copyright,
        )

    def _generate_source_infocomments(self):
        self.project.report("Generating source infocomments")

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

        lines = split_into_lines(raw_comment)
        return "\r\n%s\r\n// " % "\r\n".join(["// " + x for x in lines])

    def _generate_vs_project_file(self):
        self.project.report("Generating VS proj file")

        proj_file_name = "%s.csproj" % self.project.full_name

        self.project.write_template(
            proj_file_name, "templates/cs/vs-cs-lib.TEMPLATE.csproj",
            guid=self.project_guid,
            assembly_name=self.project.full_name,
            root_namespace=self.project.name,
            compile_list=self._generate_csproj_compile_part()
        )

    def _generate_csproj_compile_part(self):
        return "\r\n".join(["    <Compile Include=\"%s\" />" % x.replace('/', '\\') for x in self.source_files])
