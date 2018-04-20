#!/bin/bash

set -e

SQLDIR='/home/matt/git/tickets_parser/sql'

function sql_from_file {
    echo "running $SQLDIR/$1" 
    psql -p5432 -d tickets -U tickets < $SQLDIR/$1 
}

function setup_db {
    echo "restarting postgres"
    sudo service postgresql restart

    echo "Reinitializing database"
    sudo su postgres -c "psql -p 5432 < $SQLDIR/init_db.sql"
    sql_from_file create_tables.sql
}

#setup_db
./parser.py
