#!/usr/bin/env bash

# A script that runs database upgrades.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "${ROOT}/scripts/shflags"

DEFINE_string "db_envroot" "$ROOT/db/env" "The DB migrations environment root." "d"
DEFINE_string "db_type" "sqlite" "The type of database to use." "t"
DEFINE_string "db_user" "uwsolar" "The database user." "u"
DEFINE_string "db_password" "" "The database password." "P"
DEFINE_string "db_host" ":memory:" "The database host." "H"
DEFINE_string "db_name" "uwsolar" "The database name." "n"

FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

set -e
set -o posix

echo -e "\e[1;45mMigrating database...\e[0m"

source "${FLAGS_db_envroot}/bin/activate"
alembic -c "$ROOT/db/migration/alembic.ini" \
  -x db_type=${FLAGS_db_type} \
  -x db_user=${FLAGS_db_user} \
  -x db_password=${FLAGS_db_password} \
  -x db_host=${FLAGS_db_host} \
  -x db_name=${FLAGS_db_name} \
  upgrade head
deactivate
