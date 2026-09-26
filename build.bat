@echo off
setlocal
cd /d "%~dp0"
set "BUILD_PY=%~dp0.build-venv\Scripts\python.exe"

if exist "%BUILD_PY%" goto install
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -m venv "%~dp0.build-venv"
) else (
    python -m venv "%~dp0.build-venv"
)
if errorlevel 1 goto failed

:install
echo [1/2] Installing build dependencies...
"%BUILD_PY%" -m pip install --disable-pip-version-check -r "%~dp0requirements-build.txt"
if errorlevel 1 goto failed

echo [2/2] Building standalone BigTwo.exe...
"%BUILD_PY%" -m PyInstaller --noconfirm "%~dp0BigTwo.spec"
if errorlevel 1 goto failed
if not exist "%~dp0dist\BigTwo.exe" goto failed

echo.
echo Build succeeded: "%~dp0dist\BigTwo.exe"
echo All game images and the fallback font are embedded in this EXE.
echo Copy only BigTwo.exe to another Windows computer to play.
if /i not "%~1"=="--no-pause" pause
exit /b 0

:failed
echo.
echo Build failed. Check the error above.
echo Python 3.10 or newer and internet access for dependency installation are required.
if /i not "%~1"=="--no-pause" pause
exit /b 1
