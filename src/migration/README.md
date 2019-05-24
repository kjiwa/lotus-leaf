# Energy Meter Data Collector

## Database Migration Scripts

Database migration scripts allow changes to database schemas to be rolled out
incrementally and gracefully. We use the Alembic toolkit
(http://alembic.zzzcomputing.com/en/latest/) for changes to the EMDC schema.

### Requirements

Python 3 must be present before DB migration can occur. All databases supported
by SQLAlchemy are supported, though MariaDB/MySQL and SQLite3 are given primary
support in our application.

### Running

The script, `migrate.py`, sets up the Python environment and passes custom DB
flags to Alembic.

```bash
(env) migration$ python migrate.py --db_host=sqlite.db
```

More fine-grained control over DB migrations can be had by directly executing
Alembic.

```bash
(env) $ alembic -c src/migration/alembic.ini -x db_host=sqlite.db upgrade head
```

The key command being executed is ```alembic upgrade head```, which inspects
the database and applies any updates required to make it current.

### Options

By default, the DB migration scripts are configured to connect to SQLite with
the following connection string:
"${db_type}://${db_user}:${db_password}@${db_host}:${db_port}/${db_name}."

* db_type: The database protocol and driver, "sqlite" by default.
* db_user: The database user, "uwsolar" by default.
* db_password: The database password, blank by default.
* db_host: The database hostname, ":memory:" by default.
* db_port: The database port, 3306 by default.
* db_name: The database name, "uwsolar" by default.

To set these variables, run the migration with the following flags:

```bash
(env) migration$ python migrate.py --db_host=mysql+mysqlconnector --db_host=localhost
```
