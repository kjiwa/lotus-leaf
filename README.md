# UW Solar Power Monitor

## Data Collection Server

The ```collector``` directory contains a WSGI service that connects to a solar panel instance. The server may be queried to retrieve data from the solar panel and write the values to a database.

## Database Utilities

The following scripts and utilities help manage and interact with the Solar Power Monitor database:

1. The ```gendata``` directory contains a tool that can be used to populate the database with sample data.
2. The ```migration``` directory contains scripts that can be used to make incremental changes to the database schema.
3. The ```sql``` directory contains sample SQL scripts that were used to create the original database schema.

## Installation

In a python3 environment do the following to get the collector up and running.

`pip install -r requirements.txt`

Navigate to the `src` directory and run the `main.py` file with the following arguments.

- `panel_host` = The solar panel host address.
- `panel_topic_prefix` = The solar panel topic prefix.
- `panel_metrics_workbook` = The workbook containing solar panel metrics data.

Example:

```bash
$ cd lotus-leaf
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ cd src
(env)$ PYTHONPATH=. python collector/main.py --panel_host=10.154.120.13 --panel_topic_prefix=UW/Mercer/nexus_meter --panel_metrics_workbook=collector/maps/nexus-metrics.xlsx
```
