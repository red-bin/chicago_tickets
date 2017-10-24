# chicago_tickets
Project to parse and map 38 million parking tickets from 2003 and 2016. The information itself came from a Chicago Department of Revenue FOIA request.

### Design Goals
Throwing out data is a last resort option.
Repeatability, always.
PostgREST + psql views = simple api interface.
Filetype (eg, json/csv) serialization should be easy.
SQL first, python second.

### Cleanup Woes
The FOIA data received through FOIA is bombastically messy.
An address string is the only useful location info.
Addresses are free-form, with many, many millions of typos.
Data is semicolon separated, and typos contain semicolons.
Good address correction is expensive.
Free/cheap correction isn't very good.

### Data normalization state
Addresses are categorized using usaddresses and updated into the table, `ticket_addrs`.
Lat/long is currently not associated with ticket addresses.
Address suffixes are normalized with lookups from `corrections` table.
A normalized levenstein distance of less than .2 is used for typos correction.
Rogue quote chars break import of many ticket lines.

### Data normalization Todo
OSM+PostGIS for address lookups in place of data.cityofchicago.org data.
Implement typo validation using time delta between tickets from ticketers.
Add timeseries functionality, either through psql extension or influxdb.
Train usaddresses against Chicago addresses only.
Improve upon nlevenstein address correction.
Add url of legal code into `violations` table.
Add cost into `violations` table.
Validate address correction.
Add indexes to tables.

### Pipe dream
Audit whether a ticket should have been given or not.

### Design Todo
Makefile
Improve documentation.
Remove my local dependencies.
Create a web page.
Trello?
Docker?
