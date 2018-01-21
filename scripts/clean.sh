#!/usr/bin/env bash

# A script that removes dependencies, build artifacts, and temporary files.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "envroot" "$ROOT/src/server/env" "The server environment root." "e"
DEFINE_string "db_envroot" "$ROOT/db/env" "The DB migrations environment root." "d"
DEFINE_boolean "delete_shflags" ${FLAGS_TRUE} "Whether to delete shflags." "s"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mCleaning build artifacts...\e[0m"

# Remove shflags.
if [ ${FLAGS_delete_shflags} -eq ${FLAGS_TRUE} ]; then
  pushd "$ROOT/scripts"
  rm -f shflags-real
  popd
fi

rm -rf "$ROOT/dist"
rm -rf "$ROOT/src/client/node_modules" "$ROOT/src/client/package-lock.json"
rm -rf "${FLAGS_envroot}"
rm -rf "${FLAGS_db_envroot}"

find "$ROOT" -type d -name "__pycache__" -exec rm -rf {} \; 2> /dev/null || true
find "$ROOT" -type f -name "*.pyc" -delete
find "$ROOT" -type f -name "*~" -delete
rm -f .coverage
