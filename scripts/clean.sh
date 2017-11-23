#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

rm -rf "${FLAGS_envroot}"
find . -type d -name "__pycache__" -exec rm -rf {} \;
find . -type f -name "*.pyc" -delete
find . -type f -name "*~" -delete
