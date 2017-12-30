#!/usr/bin/env bash

# A script that installs build and runtime dependencies.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "envroot" "${ROOT}/env" "The environment root." "e"
DEFINE_string "db_envroot" "$ROOT/db/env" "The DB migrations environment root." "d"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mSetting up build and runtime environment...\e[0m"

# Install frontend dependencies.
echo -e "\e[1;33mInstalling frontend dependencies...\e[0m"
pushd "$ROOT/src/client"
npm install -q
popd

# Install Python dependencies.
echo -e "\e[1;33mInstalling Python dependencies...\e[0m"

python3 -m venv "${FLAGS_db_envroot}"
source "${FLAGS_db_envroot}/bin/activate"
pip install -q -r "$ROOT/db/requirements.txt"
deactivate

python3 -m venv "${FLAGS_envroot}"
source "${FLAGS_envroot}/bin/activate"
pip install -q -r "$ROOT/src/server/requirements.txt"
deactivate
