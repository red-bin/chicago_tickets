#!/bin/bash

set -e

SQLDIR="/home/matt/git/chicago_tickets/sql"
DATADIR="/home/matt/git/chicago_tickets/data/"

function sql_from_file { 
    echo "running $SQLDIR/$1" 
    time psql -p5432 -d tickets -U tickets -v datadir="$DATADIR" < $SQLDIR/$1
}

#put this into the script somehow
#egrep "(^([^;]*;){13,}[^;]*$|^([^;]*;){,11}[^;]*$)" #not enough semicolons
#egrep -v "(^([^;]*;){13,}[^;]*$|^([^;]*;){,11}[^;]*$)" #justright

#unzip -p openaddr-collected-us_midwest.zip us/il/cook.csv \
#  | awk -F',' '$6 == "Chicago" {print $1","$2","$3","$4","$9",open_addrs"}' > chicago_addresses.csv 

sudo service postgresql restart
sudo su postgres -c "psql -p 5432 < $SQLDIR/init_db.sql"

sql_from_file create_tables.sql
sql_from_file setup_triggers.sql

sql_from_file load_from_files.sql

echo "Tokenizing addresses"
utils/parse_rawaddrs.py
sql_from_file postparse.sql

utils/generate_levens.py
sql_from_file corrections.sql

#sql_from_file make_postgrest_ready.sql
