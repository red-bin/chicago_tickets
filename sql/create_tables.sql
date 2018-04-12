CREATE TABLE data_sources (
  id SERIAL PRIMARY KEY,
  alias TEXT NOT NULL,
  url TEXT NOT NULL) ; 

CREATE TABLE token_types (
  id SERIAL PRIMARY KEY,
  token_type TEXT NOT NULL) ;

CREATE TABLE levens (
  id SERIAL PRIMARY KEY,
  change_from TEXT NOT NULL,
  change_to TEXT NOT NULL,
  nleven FLOAT NOT NULL) ;

CREATE TABLE addr_tokens (
  id SERIAL PRIMARY KEY,
  token_str TEXT,
  token_type TEXT NOT NULL,
  UNIQUE (token_str, token_type)) ;

CREATE TABLE corrections (
  id SERIAL PRIMARY KEY, 
 -- change_from INTEGER REFERENCES addr_tokens(id), 
  change_from TEXT,
  change_to INTEGER REFERENCES addr_tokens(id),
  source INTEGER REFERENCES data_sources,
  UNIQUE (change_from, change_to, source)) ;

CREATE TABLE violations (
  id SERIAL PRIMARY KEY,
  code TEXT,
  description TEXT,
  cost FLOAT) ;

CREATE TABLE raw_addresses (
  id SERIAL PRIMARY KEY,
  raw_addr_id INTEGER REFERENCES addr_tokens(id),
  raw_unit_id INTEGER REFERENCES addr_tokens(id),
  raw_unit_start_id INTEGER REFERENCES addr_tokens(id),
  raw_unit_end_id INTEGER REFERENCES addr_tokens(id),
  raw_direction_id INTEGER REFERENCES addr_tokens(id),
  raw_street_name_id INTEGER REFERENCES addr_tokens(id),
  raw_suffix_id INTEGER REFERENCES addr_tokens(id),
  raw_longitude_id INTEGER REFERENCES addr_tokens(id),
  raw_latitude_id INTEGER REFERENCES addr_tokens(id),
  raw_zip_id INTEGER REFERENCES addr_tokens(id),
  correction_id INTEGER REFERENCES corrections(id),
  source_id INTEGER REFERENCES data_sources(id),
  UNIQUE (raw_addr_id, source_id)) ;

CREATE TABLE parsed_tokens (
  id SERIAL PRIMARY KEY,
  raw_addr_id INTEGER REFERENCES addr_tokens(id),
  unit_id INTEGER REFERENCES addr_tokens(id),
  dir_id INTEGER REFERENCES addr_tokens(id),
  street_id INTEGER REFERENCES addr_tokens(id),
  suffix_id INTEGER REFERENCES addr_tokens(id),
  scrap_id INTEGER REFERENCES addr_tokens(id)) ;

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  raw_addr_id INTEGER REFERENCES raw_addresses,
  unit_id INTEGER REFERENCES addr_tokens,
  dir_id INTEGER REFERENCES addr_tokens,
  name_id INTEGER REFERENCES addr_tokens,
  suffix_id INTEGER REFERENCES addr_tokens,
  scraps_id INTEGER REFERENCES addr_tokens,
  longitude_id INTEGER REFERENCES addr_tokens,
  latitude_id INTEGER REFERENCES addr_tokens) ;

CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  ticket_number BIGINT,
  violation_id INTEGER REFERENCES violations(id),
  raw_addr_id INTEGER REFERENCES raw_addresses(id),
  time TIMESTAMP,
  ticket_queue CHAR(20),
  unit CHAR(20),
  badge CHAR(10),
  license_type CHAR(20),
  license_state CHAR(5),
  license_number CHAR(15),
  car_make CHAR(20),
  hearing_dispo CHAR(20)) ;

CREATE TABLE raw_tickets (
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

CREATE TABLE chicago_addresses (
  id serial PRIMARY KEY,
  longitude FLOAT,
  latitude FLOAT,
  unit TEXT,
  raw_addr TEXT,
  zip INTEGER,
  source TEXT) ;

CREATE TABLE smartystreets (
  original TEXT,
  delivery_line_1 TEXT,
  delivery_line_2 TEXT,
  unit TEXT,
  street_predirection TEXT,
  street_name TEXT,
  street_postdirection TEXT,
  suffix TEXT,
  zipcode TEXT,
  latitude TEXT,
  longitude TEXT
) ;

CREATE TABLE street_ranges (
  id SERIAL PRIMARY KEY,
  raw_addr TEXT,
  direction CHAR(1),
  street TEXT,
  suffix CHAR(4),
  suffix_dir CHAR(2),
  unit_start INTEGER,
  unit_end INTEGER ) ;

CREATE TABLE parsed_temp (
    id SERIAL PRIMARY KEY,
    raw_addr TEXT,
    unit TEXT,
    dir TEXT,
    street_name TEXT,
    suffix TEXT,
    scrap TEXT);
