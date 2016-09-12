#!/usr/bin/python2.7

from collections import defaultdict,OrderedDict
from difflib import get_close_matches as closest
from difflib import SequenceMatcher
import re

def ratio(word1,word2):
    return SequenceMatcher(None,word1,word2).ratio()

def match_ratios(word, wordlist):
    if len(word) <= 4:
        return []

    matches = OrderedDict([ (match, ratio(word, match)) for match in closest(word, wordlist, cutoff=.70,n=5) ][1:])

    return matches

def make_matrix(sample1, sample2, function):
    matrix = defaultdict(lambda: defaultdict())

    for x in sample1:
        result = function(x,sample2)
        matrix[x] = result
         
    return matrix

def make_goodstreets():
    return  [ line.strip().lower() for line in open('goodstreets','r') ]

def topdown_compare(goodstreets, badstreets, lower_limit): 
    corrected = defaultdict(list)
    uncorrected = []

    print badstreets
    for badkey,badvals in badstreets.items():
        if badkey in goodstreets:
            continue

        for key,val in badvals:
            if val >= lower_limit and key in goodstreets and val < 1.0:
                print badkey, key
                corrected.setdefault(badkey,key)
        
    uncorrected = dict([ (key,val) for key,val in badstreets.items() if key not in corrected.keys() and val ])

    return corrected,uncorrected
    
def make_resolution(corrected, goodstreets, final_resolution):
    ret = final_resolution
    finished = False
    while not finished:
        finished=True
        for key,val in corrected.items():
            if key in ret.keys():
                continue

            if val in goodstreets:
                ret[key] = val
                finished = False

            else:
                if val in ret.keys():
                    ret = (key,val, SequenceMatcher(a=key,b=val))

        if finished:
            break

    return ret


streets = [ line.strip().lower() for line in open('badstreets','r') if re.search('^[a-z]',line)  ]
goodstreets = [ line.strip().lower() for line in open('goodstreets','r') if re.search('^[a-z]', line) and len(line.strip()) > 4] 
goodbad = make_matrix(streets,streets,match_ratios)

results = []

final_resolution = defaultdict(str)

lower_limit = .70
bottom_limit = .95

while lower_limit <= bottom_limit:
    corrected,uncorrected = topdown_compare(goodstreets, goodbad,lower_limit)
    new_goodstreet = list(set(corrected.keys() + goodstreets))
    final_resolution = make_resolution(corrected,goodstreets,final_resolution)
    print len(corrected),len(uncorrected)
    lower_limit+=.005

outfile = open('differ.csv','w+')
lowest = {}

output = []
for before,after in final_resolution.items():
    ratio = SequenceMatcher(a=before,b=after).ratio()
    output.append(','.join([before,after,str(ratio)]) + "\n")

[outfile.writeline(str(out)) for out in output] 
outfile.close()
