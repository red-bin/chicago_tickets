#!/usr/bin/python3
import csv
import sys, os
from tests import datafile_tests as filetests
import addrparse
import info_fixer

def chiaddrs(filepath, test=True):
    unparsed = []

    fh = open(filepath, 'r')
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

def raw_tickets(filepath):
    print(filepath)
    fh = open(filepath, 'r')

    reader = csv.DictReader(fh,delimiter=';')
    fieldnames = reader.fieldnames

    count = 0
    for line in reader:
        #fails = filetests.test_tktline(line, fieldnames)

        #if fails:
        #    fixed = info_fixer.fix_tktline(line, fails,fieldnames)

        #    if fixed:
        #        line = fixed
        #        fails = None
        #if fails == None:
        #    continue

        yield line
