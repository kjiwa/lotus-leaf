# A script that installs build and runtime dependencies.

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mSetting up build and runtime environment...\e[0m"

# Install frontend dependencies.
echo -e "\e[1;33mInstalling frontend dependencies...\e[0m"
pushd www
npm install
popd

# Install Python dependencies.
echo -e "\e[1;33mInstalling Python dependencies...\e[0m"
python3 -m venv "${FLAGS_envroot}"
source ${FLAGS_envroot}/bin/activate
pip install -r requirements.txt
deactivate
