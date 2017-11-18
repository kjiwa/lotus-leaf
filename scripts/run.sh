#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source ${DIR}/shflags

DEFINE_integer port 8080 "The port on which to listen for requests." "p"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

if [ ! -d env ]; then
  echo "No environment directory found. Run setup.sh."
  exit -1
fi

python3 -m venv env
source env/bin/activate
python src/main.py --debug --port=${FLAGS_port}
deactivate
