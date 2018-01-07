#!/usr/bin/env bash

# A script that runs the data generation tool.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "db_envroot" "$ROOT/db/env" "The DB migrations environment root." "d"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mMigrating database...\e[0m"

source "${FLAGS_db_envroot}/bin/activate"
PYTHONPATH="$ROOT/src/server" python "$ROOT/db/gendata/gendata.py" $@
deactivate
