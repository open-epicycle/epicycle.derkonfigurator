__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.utils import nget, xml_escape, parse_versioned_name


class NuGetPackager(object):
    def __init__(self, repository):
        self._repository = repository

        self._package_name = "%s.%s" % (self.repository.full_name, self.repository.version)
        self._dependencies = nget(self.repository.config, "nuget_dependencies", [])
        self._lib_files = {}

    @property
    def repository(self):
        return self._repository

    @property
    def package_name(self):
        return self._package_name

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def lib_files(self):
        return self._lib_files

    def configure(self):
        relevant_projects = [x for x in self.repository.projects if self._is_relevant(x)]
        self._collect_lib_files(relevant_projects)

        if not relevant_projects:
            return

        self.repository.report("Configuring NuGet packaging")

        bin_files = self._collect_bin_files(relevant_projects)

        self._generate_nuspec()
        self._generate_create_nuget_package_cmd(bin_files)

    def _collect_lib_files(self, projects):
        for framework in self.repository.configurator.supported_frameworks:
            self._lib_files[framework] = self._collect_lib_files_for_framework(projects, framework)

    def _collect_lib_files_for_framework(self, projects, framework):
        lib_files = []
        for project in projects:
            resolved_libs = [lib for lib in project.configurator.get_flattened_resolved_libs(framework) if not lib['is_auto']]

            for resolved_lib in resolved_libs:
                lib_files += resolved_lib['lib'].get_libs(resolved_lib['framework'])

        lib_files = list(set(lib_files))
        lib_files.sort()

        return lib_files

    def _generate_nuspec(self):
        self.repository.write_template(
            "package.nuspec", "templates/packaging/nuget/package.TEMPLATE.nuspec",
            id=xml_escape(self.repository.full_name),
            version=xml_escape(self.repository.version),
            title=xml_escape(self.repository.title),
            authors=xml_escape(self.repository.organization),
            owners=xml_escape(self.repository.organization),
            license_url=xml_escape(self.repository.license_url),
            project_url=xml_escape(self.repository.url),
            description=xml_escape(self.repository.description),
            summary=xml_escape(self.repository.summary),
            release_notes=xml_escape(self.repository.release_notes),
            copyright=xml_escape(self.repository.copyright),
            tags=xml_escape(self.repository.tags),
            dependencies=self._generate_nuspec_dependencies(),
        )

    def _generate_nuspec_dependencies(self):
        template = "      <dependency id=\"%s\" version=\"%s\" />"

        return "\r\n".join([template % parse_versioned_name(x) for x in self.dependencies])

    def _generate_create_nuget_package_cmd(self, bin_files):
        self.repository.write_template(
            "create_nuget_package.cmd", "templates/packaging/nuget/create_nuget_package.TEMPLATE.cmd",
            package_name=self.package_name,
            copy_bin_commands=self._generate_copy_commands(bin_files),
        )

    def _generate_copy_commands(self, bin_files):
        frameworks = self.repository.configurator.supported_frameworks

        copy_commands = []
        for framework in frameworks:
            copy_commands += [self._generate_copy_lib_command_for_file(x, framework) for x in self.lib_files[framework]]
            copy_commands += [self._generate_copy_bin_command_for_file(x, framework) for x in bin_files]

        return "\r\n".join(copy_commands)

    def _generate_copy_lib_command_for_file(self, lib_file, framework):
        return self._generate_copy_command_for_file(lib_file.replace('/', '\\'), framework)

    def _generate_copy_bin_command_for_file(self, bin_file, framework):
        source = "bin\\%s\\Release\\%s" % (framework, bin_file)
        return self._generate_copy_command_for_file(source, framework)

        return template % params

    def _generate_copy_command_for_file(self, source, framework):
        template = "xcopy %(source)s NuGetPackage\\%(package_name)s\\lib\\%(framework)s\\"

        params = {
            'source': source,
            'package_name': self.package_name,
            'framework': framework,
        }

        return template % params

    @staticmethod
    def _is_relevant(project):
        return project.kind == 'cs' and project.type == 'lib'

    @staticmethod
    def _collect_bin_files(projects):
        bin_files = []
        for x in projects:
            bin_files += x.configurator.bin_files

        return bin_files
