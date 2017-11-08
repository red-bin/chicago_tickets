#!/bin/bash

USERNAME=$USER
DBUSER=tickets
DBPASS=tickets

BASEDIR="/home/matt/git/chicago_tickets" 
DATADIR="/opt/data/tickets"
SQLDIR="$BASEDIR/sql"

STREETNAMESURL="https://data.cityofchicago.org/api/views/i6bp-fvbx/rows.csv"
OPENADDR_URL="https://s3.amazonaws.com/data.openaddresses.io/openaddr-collected-us_midwest.zip"

function sql_from_file { echo "running $SQLDIR/$1" ; sudo su postgres -c "psql -p5432 -d tickets -U tickets < $SQLDIR/$1" ; }

#put this into the script somehow
#egrep "(^([^;]*;){13,}[^;]*$|^([^;]*;){,11}[^;]*$)" /dev/shm/all_tickets.orig.txt > all_tickets.orig.txt.semicolonbad.txt &
#egrep -v "(^([^;]*;){13,}[^;]*$|^([^;]*;){,11}[^;]*$)" /dev/shm/all_tickets.orig.txt > all_tickets.orig.txt.semicolongood.txt &

#openaddr
#unzip -p openaddr-collected-us_midwest.zip us/il/cook.csv | awk -F',' '$6 == "Chicago" {print $1","$2","$3","$4","$9",open_addrs"}' > chicago_addresses.csv 

sudo su postgres -c "psql -p 5432 < $SQLDIR/init_db.sql"
sql_from_file create_tables.sql
sql_from_file load_from_files.sql

sql_from_file preparse.sql
utils/parse_rawaddrs.py
sql_from_file postparse.sql
#sql_from_file corrections.sql
#sql_from_file make_postgrest_ready.sql
