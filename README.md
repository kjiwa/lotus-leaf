# Energy Meter Data Collector

## Overview

The Energy Meter Data Collector (EMDC) is a daemon that connect to an energy
meter over a network using the Modbus TCP protocol. It was designed to
periodically query a meter for a set of metrics and record them to a database.

The daemon exposes three HTTP endpoints:

| Endpoint      | Description                                   |
|---------------|-----------------------------------------------|
| GET /ping     | Pings the server to check if it is operating. |
| GET /metric   | Retrieves the most recent value of a metric.  |
| POST /collect | Begins a data collection cycle                |

Currently an external process (e.g. a cron job) is required to trigger a data
collection cycle by calling "POST /collect." In the future, this functionality
may be integrated into the daemon directly.

## Meter Support

The Eaton Power Xpert Meter 4000 and Nexus 1272 meters are presently
supported. Support for additional meters can be added by creating spreadsheets
mapping the meter's Modbus registers to metric names. The spreadsheet should be
placed in the ```src/collector/maps``` directory. An example from the Nexus
1272 meters spreadsheet is shown below:

| Metric Name | Metric Description             | Metric Address | Metric Size | Scaling Factor | Data Type |
|-------------|--------------------------------|----------------|-------------|----------------|-----------|
| Voltage_AN  | 1s Phase A-N Voltage           | 179            | 2           | 1.52588E-05    | INT32     |
| Current_N   | 1s Neutral Current (Secondary) | 193            | 2           | 1.52588E-05    | INT32     |

In the first row, the Voltage_AN metric is mapped to Modbus register 179 on the
Nexus 1272 meter. The metric is two registers in length and should be
interpreted as a 32-bit integer. The value must be multiplied by a scaling
factor to be converted to its true value.

## Database Utilities

The following scripts and utilities help manage the EMDC database:

1. The ```gendata``` directory contains a tool that can be used to populate the
database with sample data.
2. The ```migration``` directory contains scripts that can be used to make
incremental changes to the database schema.
3. The ```sql``` directory contains sample SQL scripts that were used to create
the original database schema.

## Installation

### Virtual Environment

EMDC depends on several third-party libraries. These libraries should be
installed in a virtual environment.

```bash
$ git clone https://github.com/kjiwa/lotus-leaf.git
$ cd lotus-leaf
$ python3 -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

### Database Setup

EDMC defaults to using an in-memory SQLite database. This is so that an
instance of the daemon can be run easily out of the box. Developers may also
find using SQLite convenient since it does not require a separate installation.

Database schema changes are managed by
[Alembic](https://alembic.sqlalchemy.org).

```bash
(env) $ cd src/migration
(env) migration$ python migrate.py --db_host=sqlite.db
```

The following command can be used to prepare a MySQL database:

```bash
(env) migration$ python migrate.py --db_type=mysql+mysqlconnector --db_host=localhost
```

## Deployment

### Development

A command line client is made available for developers. The client uses the web
server built into the Bottle framework. This server is not considered
production ready and using this client should be avoided in production.

The following parameters are needed to run EMDC:

* `panel_host`: The meter host address.
* `panel_topic_prefix`: The meter topic prefix (e.g. UW/Mercer/nexus_meter).
* `panel_metrics_workbook`: The workbook containing solar panel metrics data
(e.g. collector/maps/nexus-meter.xlsx).

```bash
(env) $ cd src
(env) src$ PYTHONPATH=. python collector/main.py \
    --panel_host=10.154.120.13 \
    --panel_topic_prefix=UW/Mercer/nexus_meter \
    --panel_metrics_workbook=collector/maps/nexus-metrics.xlsx
```

### Production

It is recommended that a WSGI application server such as uWSGI be used to
deploy EMDC in production. The file `wsgi_main.py` serves as an entrypoint
for production deployments. Configuration of EMDC is done through environment
variables.
