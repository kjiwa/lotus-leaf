# UW Solar Power Monitor

A web service to show data from solar panels deployed around the University of Washington.

<p align="center">
  <img src="screenshot.png" width="640">
</p>

### Requirements

In order to build and run the web server, a few dependencies must be present:

* Bash (https://www.gnu.org/software/bash/)
* Node.js (https://nodejs.org/en/)
* Python 3 (https://www.python.org/download/releases/3.0/)
* Wget (https://www.gnu.org/software/wget/)

#### Getopt

Some users (such as those running FreeBSD or MacOS) may notice issues related to getopt.

```bash
$ scripts/run.sh
flags:WARN getopt: illegal option -- -
getopt: illegal option -- n
getopt: illegal option -- o
getopt: illegal option -- d
-e lete_shflags --
flags:FATAL unable to parse provided options with getopt.
```

These platforms do not ship with a version of getopt that supports long command arguments, so a replacement must be installed.

##### FreeBSD

A replacement getopt may be installed from the Ports Collection (https://svnweb.freebsd.org/ports/head/misc/getopt/).

```bash
$ sudo pkg install getopt
$ pushd lotus-leaf
$ PATH=/usr/local/bin:$PATH scripts/run.sh
$ popd
```

### Download

Git (https://git-scm.com) is required to download the source code.

```bash
$ git clone https://github.com/kjiwa/lotus-leaf.git
```

### Quick Start

Use ```run.sh``` to execute an optimized web server with an empty in-memory SQLite database. This script will download additional dependencies, build the source code, and run the server.

```bash
$ pushd lotus-leaf
$ scripts/run.sh
$ popd
```

#### Populating a Sample SQLite Database

For practical development, an in-memory database is not very useful, since no tables or data are present inside of it, and there is no way to fill it with data from the web application itself. Instead, the server can be configured to create a file-based SQLite database by setting the ```--db_host``` parameter to be a file path. Afterwards, the database schema can be created and filled with randomly generated data by using ```db/gendata/gendata.py```.

First, run the server and set the SQLite database path:

```bash
$ scripts/run.sh --db_host=/path/to/sqlite.db
```

Now, create the schema by using the DB migration scripts:

```bash
$ pushd lotus-leaf/db
$ source env/bin/activate
(env) $ alembic -c migration/alembic.ini -x db_type=sqlite -x db_host=/path/to/sqlite.db upgrade head
(env) $ deactivate
$ popd
```

Finally, run ```gendata``` to populate the database:

```bash
$ pushd lotus-leaf/db
$ source env/bin/activate
(env) $ python gendata/gendata.py --db_type=sqlite --db_host=/path/to/sqlite.db --input_file=gendata/sample-square.json
(env) $ deactivate
$ popd
```

See the ```gendata``` documentation for more details about how this tool works and can be customized.

#### Connecting to a MySQL Database

The server can be configured to connect to and read data from an existing MySQL installation.

```bash
$ pushd lotus-leaf
$ scripts/run.sh --db_type=mysql+mysqlconnector --db_host=localhost --db_name=uwsolar
$ popd
```

### Supported Options

```bash
$ scripts/run.sh --help
USAGE: scripts/run.sh [flags] args
flags:
  -e,--envroot:  The server environment root. (default: 'src/server/env')
  -d,--[no]debug:  Whether to build debuggable binaries and run the server in debug mode. (default: false)
  -c,--[no]clean:  Whether to clean build artifacts and temporary files. (default: true)
  -s,--[no]setup:  Whether to setup the runtime environment. (default: true)
  -b,--[no]build:  Whether to build application binaries. (default: true)
  -p,--port:  The port on which to listen for requests. (default: 8080)
  -t,--db_type:  The type of database to use. (default: 'sqlite')
  -u,--db_user:  The database user. (default: 'uwsolar')
  -P,--db_password:  The database password. (default: '')
  -H,--db_host:  The database host. (default: ':memory:')
  -n,--db_name:  The database name. (default: 'uwsolar')
  -q,--db_pool_size:  The database connection pool size. (default: 3)
  -h,--help:  show this help (default: false)
```
