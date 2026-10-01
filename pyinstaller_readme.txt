Windows one-click build:
    build.bat

Output: dist/BigTwo.exe

For automated builds:
    build.bat --no-pause

macOS / Linux isolated build:
    ./build.sh

Output: dist/BigTwo (for the build machine's OS and architecture)
Build dependencies are installed in .build-venv on all platforms.

Images, FreeSansBold.ttf, fonts/NotoSansCJKtc-Regular.otf and fonts/OFL.txt
are embedded via BigTwo.spec. Missing required resources stop the build.
Both build scripts use --clean to refresh PyInstaller's cache.
Only the EXE is needed on the target Windows machine.
See README.md for details.
