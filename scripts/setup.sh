#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

# Install stylesheet dependencies.
echo -e "\e[1;45mInstalling stylesheet dependencies...\e[0m"
pushd www/css
npm install
popd

# Install JavaScript dependencies.
echo -e "\e[1;45mInstalling JavaScript dependencies...\e[0m"
pushd www/js
npm install
popd

# Install Python dependencies.
echo -e "\e[1;45mInstalling Python dependencies...\e[0m"
python3 -m venv "${FLAGS_envroot}"
source ${FLAGS_envroot}/bin/activate
pip install -r requirements.txt
deactivate
