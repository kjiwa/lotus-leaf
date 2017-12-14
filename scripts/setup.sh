#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

# Install stylesheet dependencies.
echo "Installing stylesheet dependencies..."
pushd www/css
npm install
popd

# Install JavaScript dependencies.
echo "Installing JavaScript dependencies..."
pushd www/js
npm install
popd

# Install Python dependencies.
echo "Installing Python dependencies..."
python3 -m venv "${FLAGS_envroot}"
source env/bin/activate
pip install -r requirements.txt
deactivate
