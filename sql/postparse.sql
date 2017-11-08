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

--generalizethiskthx
INSERT INTO addr_tokens (raw_addr_id, token_str, token_type)
  SELECT at.id, pt.street_num, 'unit' 
  FROM parsed_temp pt, addr_tokens at
  WHERE pt.raw_addr = at.token_str
  AND at.token_type = 'raw_addr'
  AND pt.street_num IS NOT NULL ;

INSERT INTO addr_tokens (raw_addr_id, token_str, token_type)
  SELECT at.id, pt.street_dir, 'direction' 
  FROM parsed_temp pt, addr_tokens at
  WHERE pt.raw_addr = at.token_str
  AND at.token_type = 'raw_addr'
  AND pt.street_dir IS NOT NULL ;

INSERT INTO addr_tokens (raw_addr_id, token_str, token_type)
  SELECT at.id, pt.street_name, 'street_name' 
  FROM parsed_temp pt, addr_tokens at
  WHERE pt.raw_addr = at.token_str
  AND at.token_type = 'raw_addr'
  AND pt.street_name IS NOT NULL ;

INSERT INTO addr_tokens (raw_addr_id, token_str, token_type)
  SELECT at.id, pt.scrap_pile, 'scrap_pile' 
  FROM parsed_temp pt, addr_tokens at
  WHERE pt.raw_addr = at.token_str
  AND at.token_type = 'raw_addr' 
  AND pt.scrap_pile IS NOT NULL ;

COMMIT ;
