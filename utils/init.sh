#!/bin/bash

USERNAME=$USER
DBUSER=tickets
DBPASS=tickets

BASEDIR="/home/matt/git/chicago_tickets"

DATADIR="/opt/data/tickets"
SQLDIR="$BASEDIR/sql"

STREETNAMESURL="https://data.cityofchicago.org/api/views/i6bp-fvbx/rows.csv"

RAWTICKETFILE="$DATADIR/parking/all_tickets.orig.txt"
CHIADDRSFILE="$DATADIR/parking/all_tickets.orig.txt"

function verbose { echo -e "[VERBOSE] $*" ; }
function info    { echo -e "[INFO] $*" ; }
function warning { echo -e "[WARNING] $*" ; }

function db_setup() {
    info "Initting db"
    sudo su postgres -c "psql < $SQLDIR/init_db.sql" 
    sudo su postgres -c "psql -d tickets < $SQLDIR/create_tables.sql"
    info "db init done"
}

function dirs_setup() {
    info "Setting up dirs"
    mkdir -p /opt/data/tickets/parking
    sudo chown -R $USERNAME:$USERNAME /opt/data/tickets/parking

    sudo rm -rf $DATADIR/temp_data 2>/dev/null
    mkdir $DATADIR/temp_data
    info "Setting up dirs done"
}

function download_data() {
    wget -q -O - $STREETNAMESURL \
      | sed -r 's/^([0-9]+)[^0-9 ]+[0-9]* /\1 /' \
      | tee "$DATADIR/chicago_tickets.new.csv" > /dev/null
}

function cpu_count() { awk '$1 == "processor" {i=$NF} END {print i+1}' /proc/cpuinfo ; }

function split_by_cpus() {
    info "Splitting $1 for multithreading"
    line_count=`wc -l $1 | awk '{print $1}'`
    lines_per=$((($line_count / `cpu_count`)+1))

    header=`head -1 $1`
    
    pushd $DATADIR/temp_data
    sed 1d $1 | split -l $lines_per --additional-suffix='.split'
    find . -type f -name \*split \
      | xargs -P`cpu_count` -I{} sed -i "1s/^/$header\n/" {}
    popd
    
    mv $DATADIR/*.split $DATADIR/temp_data

    info "Splitting $1 for multithreading done"
}

function data_setup() {
    split_by_cpus $RAWTICKETFILE
    $BASEDIR/populate_nonticket_tables.py --filepath=/opt/data/tickets/chicago_addresses.csv
    $BASEDIR/tickets.py --populate
}

function setup() {
    db_setup
    dirs_setup
    #download_data
    
    data_setup
}

setup

find $DATADIR/temp_data/ -maxdepth 1 -name '*.split' -type f \
  | xargs -P`cpu_count` -I{} $BASEDIR/tickets.py --ticketfile={}
