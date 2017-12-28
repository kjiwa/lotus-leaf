# UW Solar Power Monitor

A web service to show data from solar panels deployed around the University of Washington.

<img src="screenshot.png" width="640">

# Requirements

In order to build and run the web server, a few dependencies must be installed:

* Bash (https://www.gnu.org/software/bash/)
* Node.js (https://nodejs.org/en/)
* Protocol Buffers Compiler (https://github.com/google/protobuf)
* Python 3 (https://www.python.org/download/releases/3.0/)

# Download

Git (https://git-scm.com) is required to download the source code.

```bash
$ git clone https://github.com/kjiwa/lotus-leaf.git
```

# Quick Start

Use ```run.sh``` to execute an optimized web server with sample data.

```bash
$ pushd lotus-leaf
$ scripts/run.sh
$ popd
```

The run script will download additional dependencies, build the source code, and run the server.

The server can be configured to connect to read data from a MySQL installation.

```bash
$ pushd lotus-leaf
$ scripts/run.sh --db_type=mysql --db_user=uwsolar_ro --db_host=localhost --db_name=uwsolar
$ popd
```

# Supported Options

```bash
$ scripts/run.sh --help
USAGE: scripts/run.sh [flags] args
flags:
  -e,--envroot:  The environment root. (default: '/home/kjiwa/src/github/kjiwa/lotus-leaf/env')
  -d,--[no]debug:  Whether to build debuggable binaries and run the server in debug mode. (default: false)
  -c,--[no]clean:  Whether to clean build artifacts and temporary files. (default: true)
  -s,--[no]setup:  Whether to setup the runtime environment. (default: true)
  -b,--[no]build:  Whether to build application binaries. (default: true)
  -p,--port:  The port on which to listen for requests. (default: 8080)
  -t,--db_type:  The type of database to use. (default: 'sqlite')
  -u,--db_user:  The database user. (default: 'uwsolar')
  -q,--db_password:  The database password. (default: '')
  -o,--db_host:  The database host. (default: ':memory:')
  -n,--db_name:  The database name. (default: 'uwsolar')
  -r,--db_pool_size:  The database connection pool size. (default: 3)
  -h,--help:  show this help (default: false)
```
