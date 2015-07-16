__author__ = 'Dima Potekhin'

import os
from ProjectConfigurator import ProjectConfigurator
from epicycle.derkonfigurator.externals.DotNetLib import DotNetLib
from epicycle.derkonfigurator.externals.DotNetSystemLib import DotNetSystemLib
from epicycle.derkonfigurator.utils import nget, split_into_lines, join_ipath, ipath_replace_last_part
from epicycle.derkonfigurator.temploid import resolve_templates, process_template


class ProjectConfiguratorCs(ProjectConfigurator):
    _SOURCE_INFOCOMMENT_INSERTOID_ID = "INFO"

    def __init__(self, project):
        super(ProjectConfiguratorCs, self).__init__(project)

        self._source_files = []

        self._project_guid = nget(self.project.config, "project_guid")
        self._assemblyinfo_guid = nget(self.project.config, "assemblyinfo_guid")
        self._external_libs = nget(self.project.config, "external_libs", [])

        self._flattened_external_libs = []
        self._flattened_resolved_libs = {}

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
    def flattened_external_libs(self):
        return self._flattened_external_libs

    @property
    def source_files(self):
        return self._source_files

    @property
    def bin_files(self):
        bin_name = self.project.full_name

        return ["%s.%s" % (bin_name, ext) for ext in ['dll', 'pdb', 'xml']]

    @property
    def main_file(self):
        return "%s.dll" % self.project.full_name

    def get_csproj_file(self, framework):
        return "%s.%s.csproj" % (self.project.full_name, framework)

    def get_flattened_resolved_libs(self, framework):
        return self._flattened_resolved_libs[framework]

    def _flatten_dependencies(self):
        transitive_external_libs = []
        for referenced_project in self.project.referenced_projects:
            transitive_external_libs += referenced_project.configurator.external_libs

        flattened_external_libs = list(set(transitive_external_libs + self.external_libs))
        flattened_external_libs.sort()

        self._flattened_external_libs = flattened_external_libs

    def _configure(self):
        self._resolve_external_libs()
        self._find_source_files()
        self._generate_assemblyinfo()
        self._generate_source_infocomments()
        self._resolve_templates()

        for framework in self.project.repository.configurator.supported_frameworks:
            self._generate_vs_project_file(framework)

    def _resolve_external_libs(self):
        for framework in self.project.repository.configurator.supported_frameworks:
            self._flattened_resolved_libs[framework] = self._resolve_external_libs_for_framework(framework)

    def _resolve_external_libs_for_framework(self, framework):
        return [self.project.repository.externals.get_dotnet_lib(framework, x) for x in self.flattened_external_libs]

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

    def _resolve_templates(self):
        for source_file in self._source_files:
            new_data = resolve_templates(
                self.project.directory.read_unicode_file(source_file),
                lambda name, params: self._provide_template(source_file, name, params))

            if new_data is not None:
                self.project.directory.write_unicode_file(source_file, new_data)

    def _provide_template(self, source_file_path, template_name, template_params):
        if template_name.endswith(".TEMPLATE"):
            template_file_path = ipath_replace_last_part(source_file_path, template_name)
            template_data = self.project.directory.read_unicode_file(template_file_path)

            resolved_template_data = process_template(template_data, template_params)

            return resolved_template_data
        else:
            return "<UNKNOWN TEMPLATE>"

    def _generate_vs_project_file(self, framework):
        self.project.report("Generating VS proj file")

        framework_version, framework_define_constant = {
            'net35': ("v3.5", "NET35"),
            'net40': ("v4.0", "NET40"),
            'net45': ("v4.5", "NET45"),
        }[framework]

        system_libs = self._collect_system_libs(framework)
        external_dlls = self._collect_external_dlls(framework)

        self.project.write_template(
            self.get_csproj_file(framework), "templates/cs/vs-cs-lib.TEMPLATE.csproj",
            guid=self.project_guid,
            framework=framework,
            framework_version=framework_version,
            framework_define_constant=framework_define_constant,
            assembly_name=self.project.full_name,
            root_namespace=self.project.name,
            compile_list=self._generate_csproj_compile_part(),
            system_libs=self._generate_csproj_system_libs_parts(system_libs),
            external_dlls=self._generate_csproj_external_libs_part(external_dlls),
            project_references=self._generate_csproj_project_references_part(framework),
        )

    def _collect_system_libs(self, framework):
        system_libs = []
        for lib in self.get_flattened_resolved_libs(framework):
            if isinstance(lib, DotNetSystemLib):
                system_libs.append(lib)

        return system_libs

    def _collect_external_dlls(self, framework):
        dll_files = []
        for lib in self.get_flattened_resolved_libs(framework):
            if not isinstance(lib, DotNetLib):
                continue

            lib_framework_files = lib.libs
            lib_framework_dll_files = [x for x in lib_framework_files if os.path.splitext(x)[1].lower() == ".dll"]
            dll_files += lib_framework_dll_files

        return dll_files

    def _generate_csproj_compile_part(self):
        template = "    <Compile Include=\"%s\" />"
        return "\r\n".join([template % self._to_vs_path(x) for x in self.source_files])

    def _generate_csproj_system_libs_parts(self, system_libs):
        template = "    <Reference Include=\"%s\" />"
        return "\r\n".join([(template % x.name) for x in system_libs])

    def _generate_csproj_external_libs_part(self, dlls):
        return "\r\n".join([self._generate_csproj_external_dll_part(x) for x in dlls])

    def _generate_csproj_external_dll_part(self, dll):
        params = {
            'name': os.path.splitext(dll.split('/')[-1])[0],
            'path': self._to_vs_path(join_ipath(self.project.to_repository_relative_path, dll)),
        }

        template = \
            "    <Reference Include=\"%(name)s\">\r\n" +\
            "      <HintPath>%(path)s</HintPath>\r\n" +\
            "    </Reference>"

        return template % params

    def _generate_csproj_project_references_part(self, framework):
        parts = [self._generate_csproj_project_single_reference_part(x, framework) for x in self.project.referenced_projects]
        return "\r\n".join(parts)

    def _generate_csproj_project_single_reference_part(self, referenced_project, framework):
        referenced_csproj = referenced_project.configurator.get_csproj_file(framework)

        params = {
            'name': referenced_project.full_name,
            'guid': referenced_project.configurator.project_guid.lower(),
            'proj_file_path': "..\\%s\\%s" % (referenced_project.full_name, referenced_csproj),
        }

        template = \
            "    <ProjectReference Include=\"%(proj_file_path)s\">\r\n" +\
            "      <Project>{%(guid)s}</Project>\r\n" +\
            "      <Name>%(name)s</Name>\r\n" +\
            "    </ProjectReference>"

        return template % params

    @staticmethod
    def _to_vs_path(path):
        return path.replace('/', '\\')