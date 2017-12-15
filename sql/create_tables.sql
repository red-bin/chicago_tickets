CREATE TABLE data_sources (
  id SERIAL PRIMARY KEY,
  alias TEXT,
  url TEXT) ; 

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
  token_type TEXT,
  source TEXT,
  metadata JSONB,
  UNIQUE (change_from, change_to, token_type, source)) ;

CREATE TABLE addr_tokens (
  id SERIAL PRIMARY KEY,
  token_str TEXT,
  token_type TEXT,
  correction_id INTEGER REFERENCES corrections ) ;

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
  scrap_id INTEGER REFERENCES addr_tokens(id),
  UNIQUE (raw_addr_id));

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
