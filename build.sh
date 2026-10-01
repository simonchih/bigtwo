#!/bin/sh
# Build a standalone executable using an isolated Python environment.
set -eu
cd "$(dirname "$0")"
BUILD_PY="$PWD/.build-venv/bin/python"

if [ ! -x "$BUILD_PY" ]; then
    "${PYTHON:-python3}" -m venv .build-venv
fi

echo '[1/2] Installing build dependencies...'
"$BUILD_PY" -m pip install --disable-pip-version-check -r requirements-build.txt

echo '[2/2] Building standalone BigTwo...'
"$BUILD_PY" -m PyInstaller --clean --noconfirm BigTwo.spec
test -x dist/BigTwo

echo "Build succeeded: $PWD/dist/BigTwo"
echo 'All game images, Traditional Chinese font and font license are embedded.'
echo 'Copy BigTwo to another computer with the same OS and architecture to play.'
