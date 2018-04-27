#!/bin/bash
set -e

# Because both template1 and the user postgres database have already been created,
# we need to create the hstore extension in template1 and then recreate the postgres database.
#
# Running CREATE EXTENSION in both template1 and postgres can lead to
# the extensions having different eid's.
psql --dbname template1 -U postgres <<EOSQL
    CREATE EXTENSION hstore;
    CREATE EXTENSION ltree;
    CREATE EXTENSION pg_trgm;
    DROP DATABASE $POSTGRES_USER;
    CREATE DATABASE $POSTGRES_USER TEMPLATE template1;
EOSQL

