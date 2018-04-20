CREATE TABLE violations (
  id SERIAL PRIMARY KEY,
  code TEXT,
  description TEXT,
  cost FLOAT) ;

CREATE TABLE raw_tickets (
 ticket_number TEXT,
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

CREATE TABLE tickets (
  issue_date TIMESTAMP,
  violation_code TEXT,
  badge TEXT,
  hearing_dispo TEXT,
  unit_no TEXT,
  street_dir TEXT,
  street_name TEXT,
  street_suffix TEXT,
  latitude FLOAT,
  longitude FLOAT) ;
