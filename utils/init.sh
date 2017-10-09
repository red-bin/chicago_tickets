#!/bin/bash

USERNAME=$USER
DBUSER=tickets
DBPASS=tickets

BASEDIR="/home/matt/git/chicago_tickets" 
DATADIR="/opt/data/tickets"
TEMPDIR="/dev/shm/temp_data"
SQLDIR="$BASEDIR/sql"

STREETNAMESURL="https://data.cityofchicago.org/api/views/i6bp-fvbx/rows.csv"

RAWTICKETFILE="$DATADIR/parking/all_tickets.orig.txt"
TICKETSCSV="$DATADIR/parking/all_tickets.new.csv"
CHIADDRSFILE="$DATADIR/parking/all_tickets.orig.txt"

TICKETSHEADER="ticket_number,plate_number,license_state,license_type,car_make,issue_date,violation_location,violation_code,badge,unit,ticket_queue,hearing_dispo"

function verbose { echo -e "[VERBOSE] $*" ; }
function info    { echo -e "[INFO] $*" ; }
function warning { echo -e "[WARNING] $*" ; }

function cpu_count() { awk '$1 == "processor" {i=$NF} END {print i+1}' /proc/cpuinfo ; }

function sql_from_file { sudo su postgres -c "psql -p5433 -d tickets < $SQLDIR/$1" ; }

function db_setup() {
    info "Initting db"
    sudo su postgres -c "psql -p 5433 < $SQLDIR/init_db.sql" 
    sql_from_file create_tables.sql
    sql_from_file create_temp_raw_tickets.sql

    info "db init done"
}

function dirs_setup() {
    info "Setting up dirs"
    mkdir -p $TEMPDIR
    mkdir -p $DATADIR/temp_data

    sudo chown -R $USERNAME:$USERNAME /opt/data/tickets/parking

#    sudo rm -rf $DATADIR/temp_data 2>/dev/null
    mkdir -p /dev/shm/temp_data
    info "Setting up dirs done"
}

function download_data() {
    echo "street_name,dir,street,suffix,suffix_dir,start_address,end_address" >> "$DATADIR/Chicago_Street_Names.csv"
    wget -q -O - $STREETNAMESURL \
      | sed -r 's/^([0-9]+)[^0-9 ]+[0-9]* /\1 /' \
      | sed 1d \
      >> "$DATADIR/Chicago_Street_Names.csv" > /dev/null
}

function data_transforms() {
    #sql_from_file populate_parsing_tables.sql
    sql_from_file load_from_files.sql
}

function setup() {
    dirs_setup
    download_data
    
    data_setup
}

db_setup
data_transforms
