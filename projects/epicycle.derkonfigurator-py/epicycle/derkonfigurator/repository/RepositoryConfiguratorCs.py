__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.utils import nget
from RepositoryConfigurator import RepositoryConfigurator


class RepositoryConfiguratorCs(RepositoryConfigurator):
    def __init__(self, repository):
        super(RepositoryConfiguratorCs, self).__init__(repository)

        self._supported_frameworks = nget(self.repository.config, "dotnet_frameworks", [])
        self._configurations = ['Debug', 'Release']

    @property
    def supported_frameworks(self):
        return self._supported_frameworks

    @property
    def configurations(self):
        return self._configurations

    def _configure(self):
        self.repository.report("Configuring .NET repository")
        self._generate_rebuild_all_cmd()
        self._generate_nunit_files()

    def _generate_rebuild_all_cmd(self):
        template =\
            "@echo off\r\n" +\
            "\r\n" +\
            "cd %s\r\n" +\
            "%s\r\n" +\
            "\r\n" +\
            "pause\r\n"

        build_commands = []
        for framework in self.supported_frameworks:
            for configuration in self.configurations:
                data = "msbuild %s.%s.sln /t:Clean,Build /p:Configuration=%s" % (self.repository.name, framework, configuration)
                build_commands.append(data)

        data = template % (self.repository.PROJECTS_DIR, "\r\n".join(build_commands))
        self.repository.directory.write_unicode_file("rebuild_all.cmd", data)

    def _generate_nunit_files(self):
        for framework in self.supported_frameworks:
            self._generate_nunit_file(framework)

        self._generate_nunit_file(None)

    def _generate_nunit_file(self, framework):
        test_dll_names = [x.configurator.main_file for x in self.repository.projects if x.type == 'test']

        frameworks = [framework] if framework else self.supported_frameworks
        file_name = "Tests.%s.nunit" % (framework if framework else "all")

        test_dlls = ["..\\bin\\%s\\%s\\%s" % (f, c, d) for f in frameworks for d in test_dll_names for c in self.configurations]

        assemblies = "\r\n".join(["    <assembly path=\"%s\" />" % x for x in test_dlls])

        data = (\
            "<NUnitProject>\r\n" +\
            "  <Settings activeconfig=\"All\" processModel=\"Default\" domainUsage=\"Default\" />\r\n" +\
            "  <Config name=\"All\" binpathtype=\"Auto\">\r\n" +\
            "%s\r\n" +\
            "  </Config>\r\n" +\
            "</NUnitProject>\r\n") % assemblies

        self.repository.directory.subdir(self.repository.PROJECTS_DIR).write_unicode_file(file_name, data)