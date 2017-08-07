create table usaddresses_parse (
    id SERIAL PRIMARY KEY,
    token_key TEXT,
    token_val TEXT,
    position INTEGER) ;

CREATE TABLE violations (
    id SERIAL PRIMARY KEY,
    code TEXT,
    description TEXT,
    cost FLOAT) ;

CREATE TABLE chicago_addresses (
    id SERIAL PRIMARY KEY,
    address_number INTEGER,
    street_dir TEXT,
    street_name TEXT,
    street_type TEXT,
    latitude FLOAT,
    longitude FLOAT) ;

CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  ticket_id BIGINT,
  ticket_number BIGINT,
  violation_code CHAR(15),
  violation_id INTEGER REFERENCES violations (id),
  address_num INTEGER,
  addr_id INTEGER REFERENCES chicago_addresses (id),
  street_dir CHAR(10),
  street_name TEXT,
  street_type CHAR(20),
  time TIMESTAMP,
  weekday INTEGER,
  ticket_queue CHAR(20),
  unit CHAR(20),
  badge CHAR(10),
  license_type CHAR(20),
  license_state CHAR(5),
  license_number CHAR(15),
  car_make CHAR(20),
  hearing_dispo CHAR(20),
  parse_id INTEGER REFERENCES usaddresses_parse(id),
  raw_location CHAR(50)) ;

CREATE TABLE corrections (
    id SERIAL PRIMARY KEY, 
    field_type TEXT, 
    change_from TEXT, 
    change_to TEXT, 
    mod_type TEXT) ;

create table street_ranges (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    direction CHAR(1),
    street TEXT,
    suffix CHAR(4),
    suffix_dir CHAR(2),
    min_address INTEGER,
    max_address INTEGER);
    
alter table chicago_addresses owner to "tickets" ;                     
alter table tickets owner to "tickets" ;
alter table violations owner to "tickets" ;
alter table corrections owner to "tickets" ;
alter table street_ranges owner to "tickets" ;
alter table usaddresses_parse owner to "tickets" ;
