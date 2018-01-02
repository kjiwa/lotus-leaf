#!/usr/bin/env bash

# A script that builds stylesheets and JavaScript sources.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_boolean "debug" ${FLAGS_TRUE} "Whether to build debuggable artifacts." "d"
DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"
DEFINE_string "db_envroot" "$ROOT/db/env" "The DB migrations environment root." "D"
DEFINE_boolean "frontend" ${FLAGS_TRUE} "Whether to build the frontend." "f"
DEFINE_boolean "backend" ${FLAGS_TRUE} "Whether to build the backend." "b"
DEFINE_boolean "db" ${FLAGS_TRUE} "Whether to build the DB scripts." "E"
DEFINE_boolean "tests" ${FLAGS_TRUE} "Whether to build the tests." "t"

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
  echo -e "\e[1;33mLinting backend...\e[0m"
  source "${FLAGS_envroot}/bin/activate"

  SCRIPTS=$(find "$ROOT/src/server" -not -path "${FLAGS_envroot}/*" -type f -name "*.py")
  PYTHONPATH="$ROOT/src/server"\
":${FLAGS_envroot}/lib/python3.6/site-packages"\
      pylint \
          --rcfile="$ROOT/src/server/pylintrc" \
          $SCRIPTS|| true
  deactivate
fi

# Build DB scripts.
if [ ${FLAGS_db} -eq ${FLAGS_TRUE} ]; then
  echo -e "\e[1;33mLinting database scripts...\e[0m"
  source "${FLAGS_db_envroot}/bin/activate"

  SCRIPTS=$(find "$ROOT/db" -not -path "${FLAGS_db_envroot}/*" -type f -name "*.py")
  PYTHONPATH="$ROOT/db/gendata"\
":$ROOT/db/migration"\
":$ROOT/src/server"\
":${FLAGS_envroot}/lib/python3.6/site-packages"\
      pylint \
          --rcfile="$ROOT/db/pylintrc" \
          ${SCRIPTS}|| true
  deactivate
fi

# Build tests.
if [ ${FLAGS_tests} -eq ${FLAGS_TRUE} ]; then
  echo -e "\e[1;33mLinting tests...\e[0m"

  # Python tests.
  source "${FLAGS_db_envroot}/bin/activate"
  SCRIPTS=$(find "$ROOT/test/server" -type f -name "*.py")
  PYTHONPATH="$ROOT/src/server"\
":${FLAGS_envroot}/lib/python3.6/site-packages"\
      pylint \
          --rcfile="$ROOT/test/pylintrc" \
          $SCRIPTS|| true
  deactivate
fi
