CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE violations (
  code TEXT,
  description TEXT,
  cost INT) ;

CREATE TABLE addresses (
  original TEXT PRIMARY KEY,
  delivery_line_1 TEXT,
  delivery_line_2 TEXT,
  unit TEXT,
  street_predirection TEXT,
  street_name TEXT,
  suffix TEXT,
  street_postdirection TEXT,
  zipcode TEXT,
  longitude FLOAT,
  latitude FLOAT,
  neighborhood TEXT,
  ward_2003 TEXT,
  ward_2015 TEXT,
  blockce10 TEXT,
  tract_bloc TEXT,
  statefp10 TEXT,
  geoid10 TEXT,
  name10 TEXT,
  tractce10 TEXT,
  countyfp10 TEXT) ;

CREATE TABLE tickets (
 ticket_number TEXT,
 plate_number TEXT,
 license_state TEXT,
 license_type TEXT,
 car_make TEXT,
 issue_date TIMESTAMP,
 violation_location TEXT,
 violation_code TEXT,
 violation_desc TEXT,
 badge TEXT,
 unit TEXT,
 ticket_queue TEXT,
 hearing_dispo TEXT) ;

SELECT create_hypertable('tickets', 'issue_date');

