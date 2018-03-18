BEGIN ;

CREATE OR REPLACE FUNCTION smartystreets_post_update()
  RETURNS TRIGGER AS $$
DECLARE
  new_raw_addr_id int ;
  new_unit_id int ;
  new_unit_start_id int ;
  new_unit_end_id int ;
  new_direction_id int ;
  new_street_name_id int ;
  new_suffix_id int ;
  new_longitude_id int ;
  new_latitude_id int ;
  new_zip_id int ;
  new_correction_id int ;
  new_source_id int ;

BEGIN
  INSERT INTO corrections (change_from, change_to, token_type, source)
  VALUES (initcap(NEW.original), NEW.delivery_line_1, 'raw_addr', 'smartystreets')
  ON CONFLICT DO NOTHING
  RETURNING id INTO new_correction_id ;
    
  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.original, 'raw_addr')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.original
  RETURNING id into new_raw_addr_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.unit, 'unit')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.unit
  RETURNING id into new_unit_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.street_predirection, 'direction')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.street_predirection
  RETURNING id into new_direction_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.street_name, 'street_name')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.street_name
  RETURNING id into new_street_name_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.suffix, 'suffix')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.suffix
  RETURNING id into new_suffix_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.longitude, 'longitude')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.longitude
  RETURNING id into new_raw_addr_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.latitude, 'latitude')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.latitude
  RETURNING id into new_raw_addr_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.zipcode, 'zip')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.zipcode
  RETURNING id into new_raw_addr_id ;

  SELECT id FROM data_sources
  WHERE alias = 'smartystreets' 
  INTO new_source_id ;

  INSERT INTO raw_addresses (raw_addr_id, raw_unit_id, raw_direction_id, raw_street_name_id, raw_suffix_id, raw_longitude_id, raw_latitude_id, raw_zip_id, correction_id, source_id)
  (SELECT new_raw_addr_id, new_unit_id,
          new_direction_id, new_street_name_id, 
          new_suffix_id, new_longitude_id, 
          new_latitude_id, new_zip_id, 
          new_correction_id, new_source_id)
  ON CONFLICT DO NOTHING ;
  RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

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

CREATE TRIGGER smartystreets_trigger AFTER INSERT ON smartystreets
  FOR EACH ROW EXECUTE PROCEDURE smartystreets_post_update();

COPY smartystreets (original,delivery_line_1,delivery_line_2,unit,street_predirection,street_name,street_postdirection,suffix,zipcode,latitude,longitude)
  FROM '/home/matt/git/chicago_tickets/data/smartystreet_test.csv'
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

CREATE INDEX corrections_idx ON corrections(change_from);

COMMIT ;
--UPDATE raw_addresses
--SET correction_id = c.id
--FROM corrections c
--WHERE c.change_from = raw_addr 
--AND raw_addresses.source = 'tickets' ;
--COMMIT ;

--INSERT INTO corrections
  --(change_from, change_to, token_type_id, mod_type)
  --(SELECT change_from, change_to, tt.id, 'levens'
   --FROM levens l, token_types tt
   --WHERE tt.token_type = 'suffix');
--
--COPY corrections (token_type_id, change_from, change_to, mod_type)
  --FROM '/home/matt/git/chicago_tickets/data/corrections/street_type_handtyped.csv'
  --WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;
--
--UPDATE addresses
  --SET street_type = c.change_to
  --FROM corrections c, token_types tt 
  --WHERE c.change_from = street_type
  --AND tt.token_type = 'suffix' 
  --AND corrections.token_type_id = tt.id
  --AND street_type != '' ;
--
--UPDATE addresses
  --SET street_type = c.change_to
  --FROM corrections c, token_types tt 
  --WHERE c.change_from = street_type
  --AND tt.token_type = 'name' 
  --AND corrections.token_type_id = tt.id
  --AND street_type != '' ;
--
----UPDATE addresses
  ----SET street_type = sq.suffix
  ----FROM (SELECT distinct(s1.street), s1.suffix, s1.min_address, s1.max_address
          ----FROM street_ranges s1,
          ----(SELECT street, count(distinct(suffix)) AS suffix_count
            ----FROM street_ranges GROUP BY street) s2
            ----WHERE s1.street = s2.street 
          ----AND s2.suffix_count = 1) sq,
          ----data_sources ds
--
  ----WHERE sq.street = addresses.street_name
  ----AND addresses.street_type IS NULL 
  ----AND addresses.street_num >= sq.min_address
  ----AND addresses.street_num <= sq.max_address ;
  ----AND addresses.data_source = ds.id
  ----AND ds.alias in ('tickets', 'openaddr')
--
------COMMIT ;
