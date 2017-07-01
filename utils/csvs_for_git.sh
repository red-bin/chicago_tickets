#!/bin/bash

DUMPPATH='/opt/data/tickets/csv_dumps/'

function dump_to_file { 
    echo "copy (Select * From $1) To '$DUMPPATH/$1' With CSV DELIMITER ',' ;" | psql -d tickets
    gzip $DUMPPATH/$1.csv
}

for t in "corrections" "street_ranges" "violations" "tickets" ; do
    dump_to_file $t
done
