#!/bin/bash

set -e

# TODO(kjiwa): Use flags instead of constants.

if [ ! -d env ]; then
  echo "No environment directory found. Run setup.sh."
  exit -1
fi

python3 -m venv env
source env/bin/activate
python src/main.py --debug --port=8080
deactivate
