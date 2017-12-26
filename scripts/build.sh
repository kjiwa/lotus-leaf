# A script that builds stylesheets and JavaScript sources.

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_boolean "debug" "${FLAGS_TRUE}" "Whether to build debuggable artifacts." "d"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

if [ "${FLAGS_debug}" -eq "${FLAGS_TRUE}" ]; then
  CONFIG_FILE=webpack.development.js
else
  CONFIG_FILE=webpack.production.js
fi

echo -e "\e[1;45mBuilding frontend...\e[0m"
pushd $DIR/../www
npm run webpack -- --progress --config $CONFIG_FILE
popd
