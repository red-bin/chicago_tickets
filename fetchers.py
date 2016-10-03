#!/usr/bin/python2.7
import csv
import sys, os
import cfg
from tests import datafile_tests as filetests
import addrparse
import info_fixer

#Module is to import and run basic validations on inputs. 

def chiaddrs(n=None, fixbad=cfg.fix_chiaddrs, test=True):
    unparsed = []

    fh = open(cfg.chiaddrs,'r')
    reader = csv.DictReader(fh)

    count = 1
    for line in reader:
        testpass = filetests.test_chiaddrs(line)

        if not testpass:
           if fixbad:
               line = addrparse.correct_chiaddr(line)
           else:
               continue

        unparsed.append(line)

        if count >= n:
            break

        count+=1

    return unparsed

def raw_tickets(n=None, fix=cfg.fix_tktaddrs, test=True):
    fh = open(cfg.raw_tickets,'r')

    reader = csv.DictReader(fh,delimiter=';')
    fieldnames = reader.fieldnames

    count = 1
    for line in reader:
        if count > n:
            break

        warnings, fails = filetests.test_tktline(line, fieldnames)

        if fails and fix:
            fixed = info_fixer.fix_tktline(line, fails,fieldnames)

            if fixed:
                line = fixed
                fails = None

        count+=1
        yield line
