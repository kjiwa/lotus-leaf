-- This file contains the SQL commands necessary to prepare an existing MySQL
-- database for use with alembic migrations. Execute these commands first,
-- before using alembic for migrations.
--
--   $ mysql -u uwsolar uwsolar < init.sql

create table alembic_version (
  version_num varchar(32) not null,
  primary key (version_num)
);

insert into alembic_version (version_num) values ('b80fb9e8acd7');
