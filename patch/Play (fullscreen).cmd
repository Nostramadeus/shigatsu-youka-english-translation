@echo off
rem Optional: starts Magpie (free window upscaler, github.com/Blinue/Magpie) in the tray, then the game.
rem Leave the game on WINDOW mode; Magpie draws it full screen. Toggle scaling: Alt+Shift+A.
rem Magpie is looked for in a "Magpie" folder next to this file, then in the usual install folders.
rem If it is not found, the game starts windowed and nothing else happens.
setlocal
set "MAGPIE="
if exist "%~dp0Magpie\Magpie.exe" set "MAGPIE=%~dp0Magpie\Magpie.exe"
if not defined MAGPIE if exist "%ProgramFiles%\Magpie\Magpie.exe" set "MAGPIE=%ProgramFiles%\Magpie\Magpie.exe"
if not defined MAGPIE if exist "%LOCALAPPDATA%\Programs\Magpie\Magpie.exe" set "MAGPIE=%LOCALAPPDATA%\Programs\Magpie\Magpie.exe"
if not defined MAGPIE (
  echo Magpie not found. Starting the game windowed.
  echo For full screen: download Magpie from github.com/Blinue/Magpie and unzip it into a folder named Magpie next to this file.
) else (
  tasklist /FI "IMAGENAME eq Magpie.exe" | find /I "Magpie.exe" >nul
  if errorlevel 1 start "" "%MAGPIE%" -t
)
cd /d "%~dp0"
for %%f in ("%~dp0*.exe") do start "" "%%~ff"
