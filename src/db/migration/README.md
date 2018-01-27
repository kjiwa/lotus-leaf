# UW Solar Power Monitor

## Database Migration Scripts

Database migration scripts allow changes to database schemas to be rolled out incrementally and gracefully. We use the Alembic toolkit (http://alembic.zzzcomputing.com/en/latest/) for changes to the uwsolar schema.

### Requirements

The following dependencies must be present before DB migration can occur:

* MariaDB (https://mariadb.org/) or MySQL (https://www.mysql.com/)
* Python 3 (https://www.python.org/)

### Running

The script, ```scripts/db-migrate.sh```, sets up the Python environment and passes custom DB flags to Alembic.

```bash
$ scripts/db-migrate.sh --db_host=sqlite.db
```

More fine-grained control over DB migrations can be had by directly executing Alembic.

```bash
$ source db/env/bin/activate
(env) $ alembic -c db/migration/alembic.ini -x db_host=sqlite.db upgrade head
(env) $ deactivate
```

The key command being executed is ```alembic upgrade head```, which inspects the database and applies any updates required to make it current.

### Options

By default, the DB migration scripts are configured to connect to MySQL with the following connection string: "${db_type}://${db_user}:${db_password}@${db_host}:${db_port}/${db_name}."

* db_type: The database protocol and driver, mysql+mysqlconnector by default.
* db_user: The database user, uwsolar by default.
* db_password: The database password, blank by default.
* db_host: The database hostname, localhost by default.
* db_port: The database port, 3306 by default.
* db_name: The database name, uwsolar by default.

To set these variables, run Alembic with the following flags:

```bash
(env) $ alembic -x db_user=uwsolar_ro -x db_name=uwsolar_test upgrade head
```

### Migrating Existing Databases

If there is an existing database installation, it must be prepared for use with Alembic by executing the expressions in ```init.sql```.

```bash
$ mysql -u uwsolar uwsolar < init.sql
```

The commands in ```init.sql``` create a table called ```alembic_versions``` and add a row that sets the current database version. For subsequent invocations, first ensure that a Python environment with the dependencies listed in ```requirements.txt``` is available (this can be created by running `setup.sh`).
