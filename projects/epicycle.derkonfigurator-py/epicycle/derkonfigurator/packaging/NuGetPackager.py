__author__ = 'Dima Potekhin'


class NuGetPackager(object):
    def __init__(self, repository):
        self._repository = repository

        self._package_name = "%s.%s" % (self.repository.name, self.repository.version)

    @property
    def repository(self):
        return self._repository

    @property
    def package_name(self):
        return self._package_name

    def configure(self):
        relevant_projects = [x for x in self.repository.projects if self._is_relevant(x)]

        if not relevant_projects:
            return

        self.repository.report("Configuring NuGet packaging")

        bin_files = self._collect_bin_files(relevant_projects)

        self._generate_create_nuget_package_cmd(bin_files)

    def _generate_create_nuget_package_cmd(self, bin_files):
        self.repository.write_template(
            "create_nuget_package.cmd", "templates/packaging/nuget/create_nuget_package.TEMPLATE.cmd",
            package_name=self.package_name,
            copy_bin_commands=self._generate_copy_bin_commands(bin_files),
        )

    def _generate_copy_bin_commands(self, bin_files):
        frameworks = ['net35', 'net40', 'net45']

        return "\r\n".join([self._generate_copy_bin_commands_for_framework(bin_files, x) for x in frameworks])

    def _generate_copy_bin_commands_for_framework(self, bin_files, framework):
        return "\r\n".join([self._generate_copy_bin_commands_for_file(x, framework) for x in bin_files])

    def _generate_copy_bin_commands_for_file(self, bin_file, framework):
        template = "xcopy bin\\%(framework)s\\Release\\%(bin_file)s NuGetPackage\\%(package_name)s\\lib\\%(framework)s\\"

        params = {
            'package_name': self.package_name,
            'framework': framework,
            'bin_file': bin_file,
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
