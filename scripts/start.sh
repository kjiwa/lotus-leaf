#!/usr/bin/env bash

# A script that sets up the environment and runs the web server.
#
# The script has several flags that can be used to control program behavior, as
# well as convenience flags to automatically invoke the setup and build scripts.
#
# By default, the script will install dependencies, build the source code with
# optimizations, and run the server. The web server will use an in-memory
# database initialized with sample data, and listen for requests on port 8080.
#
# For new developers, it is recommended to run this script once without any
# arguments to ensure that the application builds and runs correctly. Subsequent
# invocations can simply invoke run.sh (or any other stage, as required) to
# decrease the build time.
#
# The following commands create a new SQLite database, populate it with
# generated data, and then starts the web server.
#
#   $ scripts/db-migrate.sh --db_host=sqlite.db
#   $ scripts/db-gendata.sh -- --db_host=sqlite.db --input_file=db/gendata/sample-cos.json
#   $ scripts/start.sh -- --db_host=sqlite.db

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "envroot" "${ROOT}/src/server/env" "The server environment root." "e"
DEFINE_boolean "debug" ${FLAGS_FALSE} "Whether to build debuggable binaries." "d"
DEFINE_boolean "clean" ${FLAGS_TRUE} "Whether to clean build artifacts and temporary files." "c"
DEFINE_boolean "setup" ${FLAGS_TRUE} "Whether to setup the runtime environment." "s"
DEFINE_boolean "build" ${FLAGS_TRUE} "Whether to build application binaries." "b"
DEFINE_boolean "run" ${FLAGS_TRUE} "Whether to run the application." "r"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

# Clean build artifacts.
if [ ${FLAGS_clean} -eq ${FLAGS_TRUE} ]; then
  "$ROOT/scripts/clean.sh" --nodelete_shflags
fi

# Install build and runtime dependencies.
if [ ${FLAGS_setup} -eq ${FLAGS_TRUE} ]; then
  "$ROOT/scripts/setup.sh"
fi

# Build project.
if [ ${FLAGS_build} -eq ${FLAGS_TRUE} ]; then
  if [ ${FLAGS_debug} -eq ${FLAGS_FALSE} ]; then
    BUILD_DEBUG_FLAG="--nodebug"
  fi

  "$ROOT/scripts/build.sh" $BUILD_DEBUG_FLAG
fi

# Run the web server.
if [ ${FLAGS_run} -eq ${FLAGS_TRUE} ]; then
  "$ROOT/scripts/run.sh" --envroot="${FLAGS_envroot}" -- $@
fi
