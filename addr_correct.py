#!/usr/bin/python3

import psycopg2
import distance

import pickle
#import usaddress
import csv

from multiprocessing import Pool

def postgres_conn():
    connstr = "port=5432 dbname=tickets host=%s user=tickets password=tickets" % "localhost"
    conn = psycopg2.connect(connstr)

    return conn


def remove_unneeded(addr):
    split = addr.split()

    try:
        if split[0].isnumeric():
            split.pop(0)

        if len(split[0]) == 1:
            split.pop(0)

    except:
        pass

    addr = ' '.join(split).lower()

    return addr

def good_streetnames(csv_path='/opt/data/tickets/Chicago_Street_Names.csv'):
    r = csv.DictReader(open(csv_path))
    csv_data = [l for l in r]

    #all street names, sans suffix, dir, unit
    ret_streets = list(set([s['street'].lower() for s in csv_data]))

    #all street names, sans direction, if it's there.
    full_streets = list(set([s['street_name'].lower() for s in csv_data]))
    new_streets = []
    for street in full_streets:
        split = street.split()
        if len(split[0]) == 1:
            street = ' '.join(split[1:])

        new_streets.append(street)

    ret_streets += list(set(new_streets))

    return ret_streets

def ticket_streetnames():
    conn = postgres_conn()
    c = conn.cursor()

    sql = """SELECT violation_location from tickets"""

    c.execute(sql)
    ticket_locations = set([a[0] for a in c.fetchall()])

    pool = Pool(processes=24)
    ticket_streets = pool.map(remove_unneeded, ticket_locations)

    return list(set(ticket_streets))

def levenshtein_row(good, bads, error_low=.1):
    rows = []
    new_goods = []
    still_bads = []

    for bad in bads:
        if abs(len(good) - len(bad)) > 3:
            continue

        if good == bad:
            continue

        dist = distance.nlevenshtein(good, bad) 
        if dist <= error_low:
            new_goods.append((good, bad, dist))

    return new_goods

def cross_levenshtein(addresses, good_streets):
    cross = {}

    bads = tuple([a for a in addresses if a not in good_streets])

    pool_vars = ((good, bads) for good in good_streets)
    pool = Pool(processes=31)
    cross = pool.starmap(levenshtein_row, pool_vars)

    return cross


def corrected_streets(fp='/home/matt/first_wave.csv'):
    r = csv.reader(open(fp,'r'))
    streets = [l[1] for l in r]

    return list(set(streets))

def corrected_streets(fp='/home/matt/first_wave.csv'):
    r = csv.reader(open(fp,'r'))
    streets = [l[1] for l in r]

    return list(set(streets))

good_streets = good_streetnames()
good_corrected_streets = corrected_streets()

ticket_streets = [ t for t in ticket_streetnames() if t not in good_streets and t not in good_corrected_streets ]

all_streets = tuple(set(ticket_streets + good_corrected_streets))

print(len(good_corrected_streets))
print(len(all_streets))

print("creating cross.")
cross = cross_levenshtein(all_streets, good_corrected_streets)


corrections = []
for c in cross:
    if not c:
        continue

    corrections += c 

bads_dict = {}
for good, bad, dist in corrections:
    if bad in bads_dict:
        if dist < bads_dict[bad][1]:
            bads_dict[bad] = (good, dist)

    else:
        bads_dict[bad] = (good, dist)

w1 = csv.writer(open('/tmp/corrections.a.csv','w'))

rows = []
for k,v in bads_dict.items():
    if v[1] <= .1:
        w1.writerow((v[0], k, v[1]))
#    elif v[1] <= .2:
#        w2.writerow((v[0], k, v[1]))
#    elif v[1] <= .3:
#        w3.writerow((v[0], k, v[1]))
#    elif v[1] <= .4:
#        w4.writerow((v[0], k, v[1]))

r = [l for l in csv.reader(open('/home/matt/first_wave.csv'))]
#second_r = csv.reader(open('/tmp/corrections.1.csv'))


#In [53]: r = [l for l in csv.reader(open('/home/matt/first_wave.csv'))]
#
#In [54]: second_r = [l for l in csv.reader(open('/tmp/corrections.1.csv'))]
#
#In [55]: new_corrects = []
#
#In [56]: for snd_good, snd_bad, snd_dist in second_r:
#    ...:     for fst_good, fst_bad, fst_dist in r:
#    ...:         if fst_bad == snd_good and fst_good != snd_bad:
#    ...:             new_corrects.append((fst_good, fst_bad, snd_bad, snd_dist))
#    ...:             
#
#In [57]: w = csv.writer(open('/tmp/next_stage.csv','w'))

#In [58]: w.writerows(new_corrects)

