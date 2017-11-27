CREATE TABLE token_types (
  id SERIAL PRIMARY KEY,
  token_type TEXT) ;

INSERT INTO token_types (token_type) VALUES
  ('raw_addr'),
  ('unit'),
  ('direction'),
  ('street_name'),
  ('suffix'),
  ('scrap'),
  ('zip') ;

CREATE TABLE levens (
  id SERIAL PRIMARY KEY,
  change_from TEXT NOT NULL,
  change_to TEXT,
  nleven FLOAT ) ;

CREATE TABLE corrections (
  id SERIAL PRIMARY KEY, 
  change_from TEXT, 
  change_to TEXT, 
  leven_id INTEGER REFERENCES levens) ;

CREATE TABLE violations (
  id SERIAL PRIMARY KEY,
  code TEXT,
  description TEXT,
  cost FLOAT) ;

CREATE TABLE raw_addresses (
  id SERIAL PRIMARY KEY,
  raw_addr TEXT,
  raw_unit TEXT,
  raw_direction TEXT,
  raw_name TEXT,
  raw_suffix TEXT,
  raw_longitude FLOAT,
  raw_latitude FLOAT,
  raw_zip INTEGER,
  source TEXT,
  UNIQUE (raw_addr, source)) ;

CREATE TABLE addr_tokens (
  id SERIAL PRIMARY KEY,
  raw_addr_id INTEGER REFERENCES raw_addresses,
  token_str TEXT,
  token_type TEXT,
  correction_id INTEGER REFERENCES corrections ) ;

CREATE TABLE data_sources (
  id SERIAL PRIMARY KEY,
  alias TEXT,
  url TEXT) ; 

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
  raw_addr_id INTEGER REFERENCES addr_tokens(id),
  time TIMESTAMP,
  ticket_queue CHAR(20),
  unit CHAR(20),
  badge CHAR(10),
  license_type CHAR(20),
  license_state CHAR(5),
  license_number CHAR(15),
  car_make CHAR(20),
  hearing_dispo CHAR(20)) ;

create table street_ranges (
  id SERIAL PRIMARY KEY,
  full_name TEXT,
  direction CHAR(1),
  street TEXT,
  suffix CHAR(4),
  suffix_dir CHAR(2),
  min_address INTEGER,
  max_address INTEGER );
