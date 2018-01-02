#!/usr/bin/env bash

# A script that runs unit tests.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"
DEFINE_string "coverage_output_dir" "${ROOT}/dist/test/coverage" "The directory where coverage reports will be written." "c"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mTesting server...\e[0m"

# Run the tests and produce a code coverage report.
source "${FLAGS_envroot}/bin/activate"
PYTHONPATH="$ROOT/src/server" \
    coverage run \
    --omit="src/server/env/*,test/server/*" \
    test/server/suite.py
coverage html -d "${FLAGS_coverage_output_dir}"
deactivate

# Run the following commands instead of those above to run unit tests in the
# Python debugger (pdb).
#source "${FLAGS_envroot}/bin/activate"
#PYTHONPATH="$ROOT/src/server" python -m pdb test/server/suite.py
#deactivate
