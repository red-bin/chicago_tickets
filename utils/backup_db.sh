#!/bin/bash

TIME=`date +\%Y\%m\%d\%H\%M` 
DUMPFILE="/opt/data/pg_backups/pg_backup.$TIME.gz"
logfile="/var/log/backups/postgres/$TIME"

gzip -c <(pg_dumpall 2>$logfile) \
     2> $logfile \
     1> $DUMPFILE
