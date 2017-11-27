
--CREATE FUNCTION insert_raw_addr(in TEXT) RETURNS integer 
--  LANGUAGE plpgsql ;
--BEGIN ;

CREATE OR REPLACE FUNCTION insertrawaddr()
RETURNS TRIGGER AS $$
  DECLARE
    raw_addr_id int;
BEGIN
  SELECT id FROM 
    (INSERT INTO raw_addresses (raw_addr, source) 
     VALUES (NEW.violation_location,'tickets') 
     RETURNING id) ;
  INTO raw_addr_id ;
  INSERT INTO tickets (ticket_number, violation_id, raw_addr_id, 
                       time, ticket_queue, unit, badge, licence_type
                       license_state, license_number, car_make, hearing_dispo)
  SELECT
    NEW.ticket_number,
    v.id,
    raw_addr_id,
    NEW.plate_number,
    NEW.license_state,
    NEW.license_type,
    NEW.car_make,
    NEW.issue_date,
    NEW.violation_location,
    NEW.violation_code,
    NEW.violation_desc,
    NEW.badge,
    NEW.unit,
    NEW.ticket_queue,
    NEW.hearing_dispo
  FROM raw_tickets r,
    violations v,
    NEW
  WHERE r.violation_location = at.token_str
    AND v.code = r.violation_code 
    AND v.description = r.violation_desc ;
  RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

\set chicago_addresses_path '\'' :datadir 'chicago_addresses.csv\''
\set tickets_path '\'' :datadir 'all_tickets.orig.txt.semicolongood.testing.txt\''
\set data_sources_path '\'' :datadir 'data_sources.csv\''
\set levens_path '\'' :datadir 'corrections/levens.csv\''
\set street_ranges_path '\'' :datadir 'street_ranges.csv\''

--import orig. tickets data into temp table
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

CREATE TRIGGER ticket_addr_trigger AFTER INSERT ON raw_tickets 
for each row EXECUTE PROCEDURE insertrawaddr();

COPY raw_tickets (ticket_number, plate_number, license_state, license_type, 
                  car_make, issue_date, violation_location, violation_code, 
                  violation_desc, badge, unit, ticket_queue, hearing_dispo)
  FROM :tickets_path
  WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ;

INSERT INTO violations (code, description, cost)
  SELECT violation_code, violation_desc, 0
   FROM raw_tickets
   GROUP BY violation_code, violation_desc ;

COPY data_sources (alias, url)
  FROM :data_sources_path
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

CREATE TEMPORARY TABLE chicago_addresses (
  id serial PRIMARY KEY,
  longitude FLOAT,
  latitude FLOAT,
  unit TEXT,
  raw_addr TEXT,
  zip INTEGER,
  source TEXT) ;

COPY chicago_addresses (longitude, latitude, unit, raw_addr, zip, source)
  FROM :chicago_addresses_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO addresses (raw_addr, raw_unit, raw_longitude, raw_latitude, raw_zip)
  SELECT raw_addr, unit, longitude, latitude, zip 
  FROM chicago_addresses ;

COPY levens (change_from, change_to, nleven)
  FROM :levens_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COPY street_ranges (full_name, direction, street, suffix,
                  suffix_dir, min_address, max_address)
  FROM :street_ranges_path
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COMMIT ;
