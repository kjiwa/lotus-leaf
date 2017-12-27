# A script that builds stylesheets and JavaScript sources.

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_boolean "debug" "${FLAGS_TRUE}" "Whether to build debuggable artifacts." "d"
DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"
DEFINE_boolean "frontend" "${FLAGS_TRUE}" "Whether to build the frontend." "f"
DEFINE_boolean "backend" "${FLAGS_TRUE}" "Whether to build the backend." "b"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mBuilding application...\e[0m"

if [ ${FLAGS_frontend} -eq ${FLAGS_TRUE} ]; then
  echo -e "\e[1;33mBuilding frontend...\e[0m"
  if [ ${FLAGS_debug} -eq ${FLAGS_TRUE} ]; then
    CONFIG_FILE=webpack.development.js
  else
    CONFIG_FILE=webpack.production.js
  fi

  pushd $DIR/../www
  npm run webpack -- --progress --config $CONFIG_FILE
  popd
fi

if [ ${FLAGS_backend} -eq ${FLAGS_TRUE} ]; then
  echo -e "\e[1;33mBuilding backend...\e[0m"
  source ${FLAGS_envroot}/bin/activate
  find src -type f -name "*.py" | xargs pylint --rcfile=$DIR/../pylintrc
  deactivate
fi
