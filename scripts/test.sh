#!/usr/bin/env bash

# A script that runs unit tests.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_boolean "debug" ${FLAGS_FALSE} "Whether to run unit tests in a debugger." "d"
DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"
DEFINE_string "db_envroot" "${ROOT}/src/db/env" "The DB environment root." "D"
DEFINE_string "coverage_output_dir" "${ROOT}/dist/test/coverage" "The directory where coverage reports will be written." "c"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mRunning tests...\e[0m"

rm -f "$ROOT/.coverage"

# Run server tests.
echo -e "\e[1;33mRunning server tests...\e[0m"

source "${FLAGS_envroot}/bin/activate"
if [ ${FLAGS_debug} -eq ${FLAGS_TRUE} ]; then
  # Run tests in a debugger.
  python -m pdb src/server/testsuite.py
else
  # Run tests with code coverage.
  coverage run -a --omit="src/server/env/*,src/server/*_test.py,src/server/test*.py" \
      src/server/testsuite.py
fi
deactivate

# Run DB tests.
echo -e "\e[1;33mRunning DB tests...\e[0m"

source "${FLAGS_db_envroot}/bin/activate"
if [ ${FLAGS_debug} -eq ${FLAGS_TRUE} ]; then
  # Run tests in a debugger.
  PYTHONPATH="$ROOT/src/server" \
      python -m pdb src/db/gendata/testsuite.py
else
  # Run tests with code coverage.
  PYTHONPATH="$ROOT/src/server" \
      coverage run -a --omit="src/db/env/*,src/db/gendata/*_test.py,src/db/gendata/test*.py,src/server/test*.py" \
          src/db/gendata/testsuite.py
fi
deactivate

# Generate coverage report.
source "${FLAGS_envroot}/bin/activate"
coverage html -d "${FLAGS_coverage_output_dir}"
deactivate
