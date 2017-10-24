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
  WITH (FORMAT CSV, DELIMITER ';', NULL '', HEADER) ;

INSERT INTO violations (code, description, cost)
  SELECT violation_code, violation_desc, 0
   FROM raw_tickets
   GROUP BY violation_code, violation_desc ;

COPY ticket_addrs (addrstr_raw, street_num, street_dir, 
                  street_name, street_type, scrap_pile)
  FROM '/home/matt/data/tickets/parsed_addresses.csv'
      WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

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
    a.id,
    to_timestamp(r.issue_date, 'MM/DD/YYYY HH12:MI am'),
    r.ticket_queue,
    r.unit,
    r.badge,
    r.license_type,
    r.license_state,
    r.plate_number,
    r.car_make,
    r.hearing_dispo
  FROM 
    raw_tickets r,
    ticket_addrs a, 
    violations v
  WHERE 
    r.violation_location = a.addrstr_raw
    and v.code = r.violation_code 
    and v.description = r.violation_desc ;

COMMIT ;

BEGIN ;
CREATE TEMPORARY TABLE raw_latlong (
  id SERIAL PRIMARY KEY,
  address TEXT,
  longitude FLOAT,
  latitude FLOAT) ;

COPY raw_latlong (address, longitude, latitude)
  FROM '/home/matt/git/chicago_tickets/data/chicago_addresses.csv'
      WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

CREATE TEMPORARY TABLE ticket_addrs_concat
  (id SERIAL PRIMARY KEY,
  ticket_addr_id BIGINT,
  concated_addr TEXT) ;

INSERT INTO ticket_addrs_concat 
  (ticket_addr_id, concated_addr)
SELECT ta.id, concat(ta.street_num, ta.street_dir, ta.street_name, ta.street_type)
FROM ticket_addrs ta ;

UPDATE ticket_addrs
SET latitude = rll.latitude, 
    longitude = rll.longitude
FROM raw_latlong as rll,
     ticket_addrs as ta,
     ticket_addrs_concat as tac
WHERE concated_addr = rll.address
AND   ta.id = tac.ticket_addr_id ;

COMMIT ;
