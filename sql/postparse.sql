BEGIN ;

\set parsed_addresses_path '\'' :datadir 'parsed_addresses.csv\''

CREATE TABLE parsed_temp (
    id SERIAL PRIMARY KEY,
    raw_addr TEXT,
    unit TEXT,
    dir TEXT,
    street_name TEXT,
    suffix TEXT,
    scrap TEXT);

CREATE OR REPLACE FUNCTION insert_parsed_tokens()
  RETURNS TRIGGER AS $$
DECLARE
  new_raw_addr_id int ;
  new_unit_id int ;
  new_dir_id int ;
  new_street_id int ;
  new_suffix_id int ;
  new_scrap_id int ;

BEGIN
  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.raw_addr, 'raw_addr')
  ON CONFLICT DO NOTHING
  RETURNING id into new_raw_addr_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.unit, 'unit')
  ON CONFLICT DO NOTHING
  RETURNING id into new_unit_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.dir, 'direction')
  ON CONFLICT DO NOTHING
  RETURNING id into new_dir_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.street_name, 'street_name')
  ON CONFLICT DO NOTHING
  RETURNING id into new_street_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.suffix, 'suffix')
  ON CONFLICT DO NOTHING
  RETURNING id into new_suffix_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.scrap, 'scrap')
  ON CONFLICT DO NOTHING
  RETURNING id into new_scrap_id ;

  INSERT INTO parsed_tokens (raw_addr_id, unit_id, dir_id, street_id, suffix_id, scrap_id)
  VALUES (new_raw_addr_id, new_unit_id, new_dir_id, new_street_id, new_suffix_id, new_scrap_id)
  ON CONFLICT DO NOTHING ;
  RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER parsed_tokens_trigger AFTER INSERT ON parsed_temp
  FOR EACH ROW EXECUTE PROCEDURE insert_parsed_tokens();

COPY parsed_temp (raw_addr, unit, dir,
                  street_name, suffix, scrap)
  FROM :parsed_addresses_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '') ;
