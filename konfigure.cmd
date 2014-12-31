@echo off
set REPODIR=%CD%
cd projects\epicycle.derkonfigurator-py
konfigurator.py %REPODIR%
chdir /d %REPODIR%
pause