#!/usr/bin/env bash

# A script that runs unit tests.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_boolean "debug" ${FLAGS_FALSE} "Whether to run unit tests in a debugger." "d"
DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"
DEFINE_string "db_envroot" "${ROOT}/db/env" "The DB environment root." "D"
DEFINE_string "coverage_output_dir" "${ROOT}/dist/test/coverage" "The directory where coverage reports will be written." "c"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mRunning tests...\e[0m"

# Run server tests.
echo -e "\e[1;33mRunning server tests...\e[0m"
source "${FLAGS_envroot}/bin/activate"

if [ ${FLAGS_debug} -eq ${FLAGS_TRUE} ]; then
  # Run tests in a debugger.
  python -m pdb test/server/suite.py
else
  # Run tests with code coverage.
  coverage run --omit="src/server/env/*,src/server/*_test.py,src/server/test*.py" \
      src/server/testsuite.py
fi

# Run DB tests.
echo -e "\e[1;33mRunning DB tests...\e[0m"
source "${FLAGS_db_envroot}/bin/activate"
PYTHONPATH="$ROOT/src/server" \
    coverage run -a --omit="db/env/*,db/gendata/*_test.py" \
        db/gendata/gendata_test.py
coverage html -d "${FLAGS_coverage_output_dir}"
deactivate
