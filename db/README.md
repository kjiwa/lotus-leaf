# UW Solar Power Monitor

## Database Migration Scripts

Database migration scripts allow changes to database schemas to be rolled out incrementally and gracefully. We use the Alembic toolkit (http://alembic.zzzcomputing.com/en/latest/).

### Requirements

The following dependencies must be present before DB migration can occur:

* MySQL (or MariaDB)
* Python 3

### Quick Start

If there is an existing MySQL installation, it must be prepared for use with Alembic by executing the expressions in init.sql.

```bash
$ mysql -u uwsolar uwsolar < init.sql
```

For subsequent invocations, first ensure that a a Python environment with the dependencies listed in requirements.txt is available.

```bash
$ pushd lotus-leaf/db
$ source env/bin/activate
(env) $ alembic upgrade head
(env) $ deactivate
$ popd
```

The key command being executed is ```alembic upgrade head```, which inspects the database and applies any updates required to make it current.

### Options

By default, the DB migration scripts are configured to connect to MySQL with the following connection string: "uwsolar@localhost/uwsolar." This string can be controlled with the following variables:

* db_user: The database user, uwsolar by default.
* db_password: The database password, blank by default.
* db_host: The database hostname, localhost by default.
* db_port: The database port, 3306 by default.
* db_name: The database name, uwsolar by default.

To set these variables, run Alembic with the following flags:

```bash
(env) $ alembic -x db_user=uwsolar_ro db_name=uwsolar_test upgrade head
```
