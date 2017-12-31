#!/usr/bin/env bash

# A script that builds stylesheets and JavaScript sources.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_boolean "debug" ${FLAGS_TRUE} "Whether to build debuggable artifacts." "d"
DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"
DEFINE_string "db_envroot" "$ROOT/db/env" "The DB migrations environment root." "g"
DEFINE_boolean "frontend" ${FLAGS_TRUE} "Whether to build the frontend." "f"
DEFINE_boolean "backend" ${FLAGS_TRUE} "Whether to build the backend." "b"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mBuilding application...\e[0m"

# Create output directory.
[ -d "$ROOT/dist" ] || mkdir "$ROOT/dist"

# Build frontend.
if [ ${FLAGS_frontend} -eq ${FLAGS_TRUE} ]; then
  # Run webpack.
  echo -e "\e[1;33mBuilding frontend...\e[0m"
  if [ ${FLAGS_debug} -eq ${FLAGS_TRUE} ]; then
    CONFIG_FILE=webpack.development.js
  else
    CONFIG_FILE=webpack.production.js
  fi

  pushd "$ROOT/src/client"
  npm run webpack -- --progress --config $CONFIG_FILE
  popd

  # Copy static resources.
  cp "$ROOT/src/client/img/favicon.ico" "$ROOT/dist/www"
fi

# Build backend.
if [ ${FLAGS_backend} -eq ${FLAGS_TRUE} ]; then
  echo -e "\e[1;33mLinting DB migrations scripts...\e[0m"
  source "${FLAGS_db_envroot}/bin/activate"
  find "$ROOT/db/alembic" -not -path "${FLAGS_db_envroot}/*" -type f -name "*.py" | xargs pylint \
    --rcfile="$ROOT/db/pylintrc" || true
  deactivate

  echo -e "\e[1;33mLinting backend...\e[0m"
  source "${FLAGS_envroot}/bin/activate"
  find "$ROOT/src/server" -not -path "${FLAGS_envroot}/*" -type f -name "*.py" | xargs pylint \
    --rcfile="$ROOT/src/server/pylintrc" || true
  deactivate
fi
