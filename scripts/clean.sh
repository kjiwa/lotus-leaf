# A script that removes dependencies, build artifacts, and temporary files.

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"
DEFINE_boolean "delete_shflags" ${FLAGS_TRUE} "Whether to delete shflags." "s"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mCleaning build artifacts...\e[0m"

# Remove shflags.
if [ ${FLAGS_delete_shflags} -eq ${FLAGS_TRUE} ]; then
  pushd scripts
  rm -f shflags-real
  popd
fi

# Remove frontend artifacts.
pushd www
rm -rf dist node_modules package-lock.json
popd

# Remove Python artifacts.
rm -rf "${FLAGS_envroot}"
find . -type d -name "__pycache__" -exec rm -rf {} \;
find . -type f -name "*.pyc" -delete

# Remove temporary files.
find . -type f -name "*~" -delete
