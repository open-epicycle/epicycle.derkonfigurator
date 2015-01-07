@echo off

rmdir NuGetPackage /s /q
mkdir NuGetPackage
mkdir NuGetPackage\%(package_name)s
mkdir NuGetPackage\%(package_name)s\lib

copy package.nuspec NuGetPackage\%(package_name)s\%(package_name)s.nuspec
copy README.md NuGetPackage\%(package_name)s\README.md
copy LICENSE NuGetPackage\%(package_name)s\LICENSE

%(copy_bin_commands)s

pause