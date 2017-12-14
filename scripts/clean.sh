#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

# Remove stylesheet artifacts.
pushd www/css
rm -rf dist node_modules
popd

# Remove JavaScript artifacts.
pushd www/js
rm -rf dist node_modules
popd

# Remove Python artifacts.
rm -rf "${FLAGS_envroot}"
find . -type d -name "__pycache__" -exec rm -rf {} \;
find . -type f -name "*.pyc" -delete

# Remove temporary files.
find . -type f -name "*~" -delete
find . -type f -name "package-lock.json" -delete
