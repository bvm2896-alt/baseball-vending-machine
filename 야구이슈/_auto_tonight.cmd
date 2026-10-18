@echo off
chcp 65001 >nul
rem 10/17: tonight's review is a LONGFORM (user). This file only starts the longform auto build (found by file name, no Korean path here).
for /d %%D in ("%~dp0..\*") do if exist "%%D\_auto_long_tonight.cmd" call "%%D\_auto_long_tonight.cmd"
