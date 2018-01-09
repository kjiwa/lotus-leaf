#!/usr/bin/env bash

# A script that runs the web server.
#
# The script has several flags that can be used to control program behavior, as
# well as convenience flags to automatically invoke the setup and build scripts.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mRunning web server...\e[0m"
python3 -m venv "${FLAGS_envroot}"
source "${FLAGS_envroot}/bin/activate"
python "$ROOT/src/server/main.py" $@
deactivate
