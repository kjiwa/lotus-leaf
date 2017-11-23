#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${DIR}/shflags"

DEFINE_string "envroot" "$DIR/../env" "The environment root." "e"
DEFINE_integer "port" 8080 "The port on which to listen for requests." "p"
DEFINE_string "db_type" "sqlite" "The type of database to use." "d"
DEFINE_string "db_user" "uwsolar" "The database user." "u"
DEFINE_string "db_password" "" "The database password." "q"
DEFINE_string "db_host" ":memory:" "The database host." "o"
DEFINE_string "db_name" "uwsolar" "The database name." "n"
DEFINE_integer "db_pool_size" 3 "The database connection pool size." "s"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e

if [ ! -d env ]; then
  echo "No environment directory found. Run setup.sh."
  exit -1
fi

python3 -m venv "${FLAGS_envroot}"
source env/bin/activate
python src/main.py \
  --debug \
  --port=${FLAGS_port} \
  --db_type=${FLAGS_db_type} \
  --db_user=${FLAGS_db_user} \
  --db_password=${FLAGS_db_password} \
  --db_host=${FLAGS_db_host} \
  --db_name=${FLAGS_db_name} \
  --db_pool_size=${FLAGS_db_pool_size}
deactivate
