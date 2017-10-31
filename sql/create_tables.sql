CREATE TABLE corrections (
    id SERIAL PRIMARY KEY, 
    field_type TEXT, 
    change_from TEXT, 
    change_to TEXT, 
    mod_type TEXT ) ;

CREATE TABLE levens (
  id SERIAL PRIMARY KEY,
  change_from TEXT,
  change_to TEXT,
  nleven FLOAT ) ;

CREATE TABLE violations (
    id SERIAL PRIMARY KEY,
    code TEXT,
    description TEXT,
    cost FLOAT) ;

CREATE TABLE chicago_addrs (
    id SERIAL PRIMARY KEY,
    addrstr_raw TEXT,
    unit TEXT,
    street_dir TEXT,
    street_name TEXT,
    street_type TEXT,
    scrap_pile TEXT,
    longitude FLOAT,
    latitude FLOAT) ;

CREATE TABLE ticket_addrs (
    id SERIAL PRIMARY KEY,
    addrstr_raw TEXT,
    addrstr_current TEXT,
    street_num INTEGER,
    street_dir TEXT,
    street_name TEXT,
    street_type TEXT,
    scrap_pile TEXT,
    chicago_addr_id INTEGER REFERENCES chicago_addrs,
    correction_id INTEGER REFERENCES corrections ) ;

CREATE TABLE tickets (
  id SERIAL PRIMARY KEY,
  ticket_number BIGINT,
  violation_id INTEGER REFERENCES violations(id),
  addr_id INTEGER REFERENCES ticket_addrs(id),
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
    max_address INTEGER);
