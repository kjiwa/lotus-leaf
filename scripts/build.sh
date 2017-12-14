# A script that builds stylesheets and JavaScript sources.

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_boolean "debug" "${FLAGS_TRUE}" "Whether to build debuggable artifacts." "d"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

# Build stylesheets.
echo -e "\e[1;45mBuilding stylesheets...\e[0m"
pushd $DIR/../www/css
if [ "${FLAGS_debug}" -eq "${FLAGS_TRUE}" ]; then
  npm run gulp package-dev
else
  npm run gulp package
fi
popd

# Build the frontend code.
echo -e "\e[1;45mBuilding JavaScript sources...\e[0m"
pushd $DIR/../www/js
if [ "${FLAGS_debug}" -eq "${FLAGS_TRUE}" ]; then
  npm run gulp package-dev
else
  npm run gulp package
fi
popd
