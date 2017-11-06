BEGIN ;

CREATE TEMPORARY TABLE raw_tickets (
  id SERIAL PRIMARY KEY,
  ticket_number BIGINT,
  plate_number TEXT,
  license_state TEXT,
  license_type TEXT,
  car_make TEXT,
  issue_date TEXT,
  violation_location TEXT,
  violation_code TEXT,
  violation_desc TEXT,
  badge TEXT,
  unit TEXT,
  ticket_queue TEXT,
  hearing_dispo TEXT) ;

COPY raw_tickets (ticket_number, plate_number, license_state, license_type, 
                  car_make, issue_date, violation_location, violation_code, 
                  violation_desc, badge, unit, ticket_queue, hearing_dispo)
  FROM '/home/matt/data/tickets/parking/all_tickets.orig.txt.semicolongood.testing.txt' 
  WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ;

INSERT INTO violations (code, description, cost)
  SELECT violation_code, violation_desc, 0
   FROM raw_tickets
   GROUP BY violation_code, violation_desc ;

COPY data_sources (alias, url)
  FROM '/home/matt/git/chicago_tickets/data/data_sources.csv'
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO addresses (raw_addr, source)
  SELECT 
    DISTINCT(rt.violation_location), 'tickets'
  FROM raw_tickets rt ;

CREATE TEMPORARY TABLE chicago_addresses (
  id serial PRIMARY KEY,
  longitude FLOAT,
  latitude FLOAT,
  unit TEXT,
  raw_addr TEXT,
  zip INTEGER,
  source TEXT) ;

COPY chicago_addresses (longitude, latitude, unit, addr, zip, source)
  FROM '/home/matt/git/chicago_tickets/data/chicago_addresses.csv'
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO addresses (raw_addr, raw_unit, raw_longitude, raw_latitude, raw_zip)
  SELECT DISTINCT(raw_addr) from chicago_addresses ca ;

COPY levens (change_from, change_to, nleven)
  FROM '/home/matt/git/chicago_tickets/data/corrections/street_name_levens.csv'
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COPY street_ranges (full_name, direction, street, suffix, suffix_dir, min_address, max_address)
  FROM '/home/matt/git/chicago_tickets/data/street_ranges.csv'
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO tickets (ticket_number, violation_id,
                     addr_id, time, ticket_queue, unit, 
                     badge, license_type, license_state, 
                     license_number, car_make, hearing_dispo)
  SELECT 
    r.ticket_number,
    v.id,
    at.id,
    to_timestamp(r.issue_date, 'MM/DD/YYYY HH12:MI am'),
    r.ticket_queue,
    r.unit,
    r.badge,
    r.license_type,
    r.license_state,
    r.plate_number,
    r.car_make,
    r.hearing_dispo
  FROM raw_tickets r,
    addr_tokens at, 
    violations v
  WHERE r.violation_location = at.token_str
    AND v.code = r.violation_code 
    AND v.description = r.violation_desc ;
COMMIT ;
