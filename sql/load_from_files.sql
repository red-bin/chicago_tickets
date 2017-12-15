BEGIN ;

CREATE OR REPLACE FUNCTION raw_tickets_insert_trigger()
  RETURNS TRIGGER AS $$
DECLARE
  raw_addr_token_id int;
  raw_addresses_id int;
BEGIN
  raw_addr_token_id := create_addr_token(NEW.violation_location, 'raw_addr') ;
  INSERT INTO raw_addresses (raw_addr_id, source_id)
  VALUES (raw_addr_token_id, NULL) 
  ON CONFLICT DO NOTHING
  RETURNING id into raw_addresses_id ;
  
  INSERT INTO tickets 
    (ticket_number, raw_addr_id, 
     time, ticket_queue, unit, badge,
     license_type, license_state, license_number, car_make, hearing_dispo)
  SELECT
    NEW.ticket_number,
    raw_addresses_id,
    to_timestamp(NEW.issue_date, 'MM/DD/YYYY HH12:MI am'),
    NEW.ticket_queue,
    NEW.unit,
    NEW.badge,
    NEW.license_type,
    NEW.license_state,
    NEW.plate_number,
    NEW.car_make,
    NEW.hearing_dispo ;
    RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION create_addr_token(new_token_str text, new_token_type text) RETURNS INT 
AS $$
DECLARE token_id int ;
BEGIN
  INSERT INTO addr_tokens (token_str, token_type) 
  VALUES (new_token_str, new_token_type)
  ON CONFLICT DO NOTHING
  RETURNING id into token_id ;
  RETURN token_id ;
END ;
$$ LANGUAGE plpgsql ;


\set chicago_addresses_path '\'' :datadir 'chicago_addresses.csv\''
\set tickets_path '\'' :datadir 'all_tickets.orig.txt.semicolongood.testing.txt\''
\set data_sources_path '\'' :datadir 'data_sources.csv\''
\set levens_path '\'' :datadir 'corrections/levens.csv\''
\set street_ranges_path '\'' :datadir 'street_ranges.csv\''

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
  FOR EACH ROW EXECUTE PROCEDURE raw_tickets_insert_trigger();

COPY data_sources (alias, url)
  FROM :data_sources_path
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COPY raw_tickets (ticket_number, plate_number, license_state, license_type, 
                  car_make, issue_date, violation_location, violation_code, 
                  violation_desc, badge, unit, ticket_queue, hearing_dispo)
  FROM :tickets_path
  WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ;

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

CREATE TEMPORARY TABLE street_ranges (
  id SERIAL PRIMARY KEY,
  raw_addr TEXT,
  direction CHAR(1),
  street TEXT,
  suffix CHAR(4),
  suffix_dir CHAR(2),
  unit_start INTEGER,
  unit_end INTEGER );

COMMIT ;
BEGIN ;
COPY street_ranges (raw_addr, direction, street, suffix,
                  suffix_dir, unit_start, unit_end)
  FROM :street_ranges_path
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COPY levens (change_from, change_to, nleven)
  FROM :levens_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COMMIT ;
