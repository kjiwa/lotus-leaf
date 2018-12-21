# UW Solar Power Monitor

## Data Collection Server

The ```collector``` directory contains a WSGI service that connects to a solar panel instance. The server may be queried to retrieve data from the solar panel and write the values to a database.

## Database Utilities

The following scripts and utilities help manage and interact with the Solar Power Monitor database:

1. The ```gendata``` directory contains a tool that can be used to populate the database with sample data.
2. The ```migration``` directory contains scripts that can be used to make incremental changes to the database schema.
3. The ```sql``` directory contains sample SQL scripts that were used to create the original database schema.
