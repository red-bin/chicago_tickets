#!/usr/bin/python3

import json
import os

from pprint import pprint

from smartystreets_python_sdk import StaticCredentials, exceptions, Batch, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

def batches_from_streets(streets, size=100):
    batches = []
    start = 0
    offset = len(streets) % size 
    params = { 'city': 'Chicago', 'state': 'Illinois', 'candidates': 5 }

    while streets:     
        batch = Batch()
        streets_batch = ( streets.pop().strip().title() for i in range(offset-start) )

        [ batch.add(Lookup(s, **params)) for s in streets_batch ]

        offset = size
        batches.append(batch)

    return batches

def streets_from_file(filepath='/home/matt/smartystreets/streets_files/streets'):
    fh = open(filepath,'r')
    streets = fh.readlines()
    fh.close()

    return streets 

def get_client():
    auth_id = "a3f33473-fc69-27c6-3e28-537ec873c146"
    auth_token = "DQrNt8KMeLn5f3PRn7wI"

    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_street_api_client()

    return client

def jsonize_batch(batch):
    ret = []
    for lookup in batch:
        candidates = lookup.result
        candidates_map = []
        for candidate in candidates:

            components = candidate.components
            metadata = candidate.metadata

            candidate_map = { 
              'unit': components.primary_number,
              'street_predirection': components.street_predirection,
              'street_name': components.street_name,
              'street_postdirection': components.street_postdirection,
              'suffix': components.street_suffix,
              'latitude': metadata.latitude,
              'longitude': metadata.longitude,
              'zipcode': "{}-{}".format(components.zipcode, components.plus4_code),
              'delivery_line_1': candidate.delivery_line_1,
              'delivery_line_2': candidate.delivery_line_2 }

            candidates_map.append(candidate_map)

        ret.append({'original': lookup.street, 'candidates':candidates_map})

    return ret

client = get_client()

batches = batches_from_streets(streets_from_file())

count = 1
for batch in batches:
    client.send_batch(batch)
    print(count, len(batches))

    count += 1

batches_results = [ jsonize_batch(batch) for batch in batches ]

results = []
for batch_results in batches_results:
    [ results.append(b) for b in batch_results ]

out_fh = open('/home/matt/results.json','w')
json.dump(results, out_fh)
out_fh.close()
