__author__ = 'Dima Potekhin'

import os
from ProjectConfigurator import ProjectConfigurator
from epicycle.derkonfigurator.utils import nget, split_into_lines, join_ipath


class ProjectConfiguratorCs(ProjectConfigurator):
    _SOURCE_INFOCOMMENT_INSERTOID_ID = "INFO"

    def __init__(self, project):
        super(ProjectConfiguratorCs, self).__init__(project)

        self._source_files = []

        self._project_guid = nget(self.project.config, "project_guid")
        self._assemblyinfo_guid = nget(self.project.config, "assemblyinfo_guid")
        self._external_libs = nget(self.project.config, "external_libs", [])

    @property
    def project_guid(self):
        return self._project_guid

    @property
    def assemblyinfo_guid(self):
        return self._assemblyinfo_guid

    @property
    def external_libs(self):
        return self._external_libs

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

        external_dlls = self._collect_external_dlls()

        proj_file_name = "%s.csproj" % self.project.full_name

        self.project.write_template(
            proj_file_name, "templates/cs/vs-cs-lib.TEMPLATE.csproj",
            guid=self.project_guid,
            assembly_name=self.project.full_name,
            root_namespace=self.project.name,
            compile_list=self._generate_csproj_compile_part(),
            external_dlls=self._generate_csproj_external_libs_part(external_dlls),
        )

    def _collect_external_dlls(self):
        platform = "net45"

        dll_files = []
        for external_lib_name in self.external_libs:
            external_lib = self.project.repository.externals.get_dotnet_lib(external_lib_name)

            lib_platform = self._find_best_platform(external_lib.available_platforms, platform)

            lib_platform_files = external_lib.get_libs(lib_platform)

            lib_platform_dll_files = [x for x in lib_platform_files if os.path.splitext(x)[1].lower() == ".dll"]
            dll_files += lib_platform_dll_files

        return dll_files

    def _find_best_platform(self, available_platforms, target_platform):
        if len(available_platforms) == 1 and available_platforms[0] == "":
            return ""

        all_platforms = ['net35', 'net40', 'net45']

        potential_platforms = all_platforms[:all_platforms.index(target_platform.lower()) + 1]
        potential_platforms.reverse()

        available_platforms_lower = [x.lower() for x in available_platforms]
        for platform in potential_platforms:
            if platform.lower() in available_platforms_lower:
                return platform

        return None

    def _generate_csproj_compile_part(self):
        template = "    <Compile Include=\"%s\" />"
        return "\r\n".join([template % self._to_vs_path(x) for x in self.source_files])

    def _generate_csproj_external_libs_part(self, dlls):
        return "\r\n".join([self._generate_csproj_external_dll_part(x) for x in dlls])

    def _generate_csproj_external_dll_part(self, dll):
        params = {
            'name': os.path.splitext(dll.split('/')[-1])[0],
            'path': self._to_vs_path(join_ipath(self.project.to_repository_relative_path, dll)),
        }

        template = "    <Reference Include=\"%(name)s\">\r\n      <HintPath>%(path)s</HintPath>\r\n    </Reference>"
        return template % params

    @staticmethod
    def _to_vs_path(path):
        return path.replace('/', '\\')