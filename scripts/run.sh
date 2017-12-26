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
# invocations can skip steps such as dependency installation and optimization
# to decrease the build time.
#
#   $ scripts/run.sh
#   $ scripts/run.sh --noclean --nosetup --debug

#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"
DEFINE_boolean "debug" ${FLAGS_FALSE} "Whether to build debuggable binaries and run the server in debug mode." "d"
DEFINE_boolean "clean" ${FLAGS_TRUE} "Whether to clean build artifacts and temporary files." "c"
DEFINE_boolean "setup" ${FLAGS_TRUE} "Whether to setup the runtime environment." "s"
DEFINE_boolean "build" ${FLAGS_TRUE} "Whether to build application binaries." "b"
DEFINE_integer "port" 8080 "The port on which to listen for requests." "p"
DEFINE_string "db_type" "sqlite" "The type of database to use." "t"
DEFINE_string "db_user" "uwsolar" "The database user." "u"
DEFINE_string "db_password" "" "The database password." "q"
DEFINE_string "db_host" ":memory:" "The database host." "o"
DEFINE_string "db_name" "uwsolar" "The database name." "n"
DEFINE_integer "db_pool_size" 3 "The database connection pool size." "r"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

if [ ${FLAGS_debug} -eq ${FLAGS_TRUE} ]; then
  BUILD_DEBUG_FLAG="--debug"
  SERVER_DEBUG_FLAG="--debug"
else
  BUILD_DEBUG_FLAG="--nodebug"
  SERVER_DEBUG_FLAG=""
fi

# Clean build artifacts.
if [ ${FLAGS_clean} -eq ${FLAGS_TRUE} ]; then
  $DIR/clean.sh
fi

# Install build and runtime dependencies.
if [ ${FLAGS_setup} -eq ${FLAGS_TRUE} ]; then
  $DIR/setup.sh
fi

# Ensure that Python dependencies have been installed.
if [ ! -d "${FLAGS_envroot}" ]; then
  echo -e "\e[91mNo environment directory found. Run setup.sh.\e[0m"
  exit -1
fi

# Build project.
if [ ${FLAGS_build} -eq ${FLAGS_TRUE} ]; then
  $DIR/build.sh $BUILD_DEBUG_FLAG
fi

# Ensure that frontend resources have been built.
if [ ! -f "$DIR/../www/dist/index.html" ]; then
  echo -e "\e[91mwww/dist/index.html not found. Run build.sh.\e[0m"
  exit -1
elif [ ! -f "$DIR/../www/dist/uwsolar.js" ]; then
  echo -e "\e[91mwww/dist/uwsolar.js not found. Run build.sh.\e[0m"
  exit -1
fi

# Run the web server.
echo -e "\e[1;45mRunning web server...\e[0m"
python3 -m venv "${FLAGS_envroot}"
source ${FLAGS_envroot}/bin/activate
python src/main.py \
  $SERVER_DEBUG_FLAG \
  --port=${FLAGS_port} \
  --db_type=${FLAGS_db_type} \
  --db_user=${FLAGS_db_user} \
  --db_password=${FLAGS_db_password} \
  --db_host=${FLAGS_db_host} \
  --db_name=${FLAGS_db_name} \
  --db_pool_size=${FLAGS_db_pool_size}
deactivate
