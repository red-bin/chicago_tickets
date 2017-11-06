BEGIN ;

CREATE TEMPORARY TABLE parsed_temp (
    id SERIAL PRIMARY KEY,
    raw_addr TEXT,
    street_num TEXT,
    street_dir TEXT,
    street_name TEXT,
    street_type TEXT,
    scrap_pile TEXT) ;

COPY parsed_temp (raw_addr, street_num, street_dir,
                  street_name, street_type, scrap_pile)
  FROM '/home/matt/git/chicago_tickets/data/parsed_addresses.csv'
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO addr_tokens (token_str, token_type)
  SELECT DISTINCT(street_num),'unit' from parsed_temp;

INSERT INTO addr_tokens (token_str, token_type)
  SELECT DISTINCT(street_dir),'direction' from parsed_temp;

INSERT INTO addr_tokens (token_str, token_type)
  SELECT DISTINCT(street_name),'street_name' from parsed_temp;

INSERT INTO addr_tokens (token_str, token_type)
  SELECT DISTINCT(street_type),'street_type' from parsed_temp;

INSERT INTO addr_tokens (token_str, token_type)
  SELECT DISTINCT(scrap_pile),'scrap_pile' from parsed_temp;

COMMIT ;
