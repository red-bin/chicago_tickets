#!/usr/bin/python2.7
import csv
import sys, os
import cfg
from tests import datafile_tests as filetests
import addrparse
import info_fixer

def chiaddrs(test=True):
    unparsed = []

    fh = open(cfg.chiaddrs,'r')
    reader = csv.DictReader(fh)

    for line in reader:
        testpass = filetests.test_chiaddrs(line)

        if not testpass:
           if fixbad:
               line = addrparse.correct_chiaddr(line)
           else:
               continue

        unparsed.append(line)

    return unparsed

def ticket_descriptions(db):
    c = db.cursor()
    c.execute("select * from violations")

    ret = [ {'code':code, 'description':description, 'cost':cost} for id, code, description, cost in c.fetchall()]
    return ret

def raw_tickets(n=1000, test=True):
    fh = open(cfg.raw_tickets,'r')

    reader = csv.DictReader(fh,delimiter=';')
    fieldnames = reader.fieldnames

    count = 0
    for line in reader:
        if count > n:
            break

        fails = filetests.test_tktline(line, fieldnames)

        if fails:
            fixed = info_fixer.fix_tktline(line, fails,fieldnames)

            if fixed:
                line = fixed
                fails = None
        if fails == None:
            continue

        yield line

