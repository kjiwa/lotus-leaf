#!/bin/bash

set -e

# TODO(kjiwa): Use flags instead of constants.

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
