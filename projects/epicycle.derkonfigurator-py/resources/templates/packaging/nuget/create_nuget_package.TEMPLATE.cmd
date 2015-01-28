@echo off

rmdir NuGetPackage /s /q
mkdir NuGetPackage
mkdir NuGetPackage\%(package_name)s
mkdir NuGetPackage\%(package_name)s\lib

copy package.nuspec NuGetPackage\%(package_name)s\%(package_name)s.nuspec
copy README.md NuGetPackage\%(package_name)s\README.md
copy LICENSE NuGetPackage\%(package_name)s\LICENSE

%(copy_bin_commands)s

cd NuGetPackage
nuget pack %(package_name)s\%(package_name)s.nuspec -Properties version=%(version)s
7z a -tzip %(package_name)s.zip %(package_name)s %(package_name)s.nupkg

echo nuget push %(package_name)s.nupkg > push.cmd
echo pause >> push.cmd

pause