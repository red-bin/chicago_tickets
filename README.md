# chicago_tickets
Project to parse and map 38 million parking tickets from 2003 and 2016. The information itself came from a Chicago Department of Revenue FOIA request.

### Design Goals
  * Throwing out data is a last resort option.<br>
  * Repeatability, always.<br>
  * PostgREST + psql views = simple api interface.<br>
  * Filetype (eg, json/csv) serialization should be easy.<br>
  * SQL first, python second.<br>

### Cleanup Woes
  * The original data is bombastically messy.</br>
  * An address string is the only useful location info.</br>
  * Addresses are free-form, with many, many millions of typos.</br>
  * Data is semicolon separated, and typos contain semicolons.</br>
  * Good address correction is expensive.</br>
  * Free/cheap correction isn't very good.</br>

### Data normalization state
  * Addresses are categorized using usaddresses and updated into the table, `ticket_addrs`.</br>
  * Lat/long is currently not associated with ticket addresses.</br>
  * Address suffixes are normalized with lookups from `corrections` table.</br>
  * A normalized levenstein distance of less than .2 is used for typos correction.</br>
  * Rogue quote chars break import of many ticket lines.</br>

### Data normalization Todo
  * OSM+PostGIS for address lookups in place of data.cityofchicago.org data.</br>
  * Implement typo validation using time delta between tickets from ticketers.</br>
  * Add timeseries functionality, either through psql extension or influxdb.</br>
  * Train usaddresses against Chicago addresses only.</br>
  * Improve upon nlevenstein address correction.</br>
  * Add url of legal code into `violations` table.</br>
  * Add cost into `violations` table.</br>
  * Validate address correction.</br>
  * Add indexes to tables.</br>

### Pipe dream
  * Audit whether a ticket should have been given or not.</br>

### Design Todo
  * Makefile</br>
  * Improve documentation.</br>
  * Remove my local dependencies.</br>
  * Create a web page.</br>
  * Trello?</br>
  * Docker?</br>
  
  ### Downloads
| Description                       | URL                                                                    | 
|------------------------|---------------------------------------------------------------------| 
| SQL Dump               | http://data.mchap.io/tickets/chicago_tickets.latest.sql.gz          | 
| Orig. from 2003-2008 | http://data.mchap.io/tickets/A50462_TcktsIssd_200303-200812.txt.gz  | 
| Orig. from 2009-2016 | http://data.mchap.io/tickets/A50462_TcktsIssdSince2009.txt.gz       | 
| Orig. from 2016-2016 | http://data.mchap.io/tickets/A50462_TcktsIssd_201603-todate.txt.gz  | 
  
