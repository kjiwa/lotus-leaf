# UW Solar Power Monitor

## Data Generation Tool

This tool generates fake data for the Solar Power Monitor database. An input file containing data generation options is required, and should be a valid JSON file containing a list of dictionaries. A basic configuration, which generates one sample every 100 seconds from the function f(x) = 1, for one day, has the form:

```json
[
  {
    "start": "2018-01-01T00:00:00.00000Z",
    "end": "2018-01-01T23:59:59.99999Z",
    "topic_id": 1,
    "topic_name": "Test Topic",
    "amplitude_offset": 1,
    "spread": 0
  }
]
```

Any ISO-8601 string is accepted for the start and end dates.

Nearly any function can be approximated, since the tool generates data based on Fourier series coefficients (i.e. by using the ```amplitude_cos``` and ```amplitude_sin``` options. Sample scripts showing square waves, sawtooth waves, and simple cosines are included.


### Quick Start

To generate square wave data, run the following commands:

```bash
$ scripts/db-gendata.sh -- --db_host=sqlite.db --input_file=src/db/gendata/sample-square.json
```

### Database Connectivity

By default, the tool will try to connect to a local, in-memory SQLite database. Database connectivity can be configured using the same set of flags present in the server for database connectivity.

To connect to a local, file-based SQLite database:

```bash
(env) $ python gendata/gendata.py \
      --input_file=src/db/gendata/sample-cos.json \
      --db_host=/path/to/sqlite.db
```

To connect to a local MySQL installation:

```bash
(env) $ python gendata/gendata.py \
      --input_file=src/db/gendata/sample-cos.json \
      --db_type=mysql+mysqlconnector \
      --db_host=localhost
```
