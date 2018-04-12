#!/bin/bash

set -e

SQLDIR="/home/matt/git/chicago_tickets/sql"
DATADIR="/home/matt/git/chicago_tickets/data"

CHI_ADDRS_PATH="$DATADIR/chicago_addresses.csv"
TICKETS_PATH="$DATADIR/all_tickets.orig.txt.semicolongood.txt"
DATA_SOURCES_PATH="$DATADIR/data_sources.csv"
LEVENS_PATH="$DATADIR/corrections/levens.csv"
STREET_RANGES_PATH="$DATADIR/street_ranges.csv"
PARSED_ADDRS_PATH="$DATADIR/parsed_addresses.csv"
SMARTY_STREETS_PATH="$DATADIR/smartystreet_successes.csv"

function test_mode {
    TICKETS_PATH="$DATADIR/all_tickets.orig.txt.semicolongood.testing.txt"
    #SMARTY_STREETS_PATH="$DATADIR/smartystreet_test.csv"
}

function sql_from_file {
    echo "running $SQLDIR/$1" 
    time psql -p5432 -d tickets -U tickets \
              -v street_ranges_path="'$STREET_RANGES_PATH'" \
              -v levens_path="'$LEVENS_PATH'" \
              -v data_sources_path="'$DATA_SOURCES_PATH'" \
              -v tickets_path="'$TICKETS_PATH'" \
              -v chicago_addresses_path="'$CHI_ADDRS_PATH'" \
              -v parsed_addresses_path="'$PARSED_ADDRS_PATH'" \
              -v smarty_streets_path="'$SMARTY_STREETS_PATH'" \
                 < $SQLDIR/$1
}

#put this into the script somehow
#egrep "(^([^;]*;){13,}[^;]*$|^([^;]*;){,11}[^;]*$)" #not enough semicolons
#egrep -v "(^([^;]*;){13,}[^;]*$|^([^;]*;){,11}[^;]*$)" #justright

#unzip -p openaddr-collected-us_midwest.zip us/il/cook.csv \
#  | awk -F',' '$6 == "Chicago" {print $1","$2","$3","$4","$9",open_addrs"}' > chicago_addresses.csv 

test_mode

echo "restarting postgres"
sudo service postgresql restart
sudo su postgres -c "psql -p 5432 < $SQLDIR/init_db.sql"

sql_from_file create_tables.sql
sql_from_file setup_triggers.sql

sql_from_file load_from_files.sql

echo "Tokenizing addresses"
time utils/parse_rawaddrs.py
sql_from_file postparse.sql

utils/generate_levens.py
sql_from_file corrections.sql

#sql_from_file make_postgrest_ready.sql
