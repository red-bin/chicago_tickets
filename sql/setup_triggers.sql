CREATE OR REPLACE FUNCTION raw_tickets_insert_trigger()
  RETURNS TRIGGER AS $$
DECLARE
  raw_addr_token_id INT ;
  raw_addresses_id INT ;
  raw_tickets_source_id INT ;
BEGIN
  SELECT id FROM data_sources
  WHERE alias = 'raw_tickets'
  INTO raw_tickets_source_id ;

  raw_addr_token_id := create_addr_token(NEW.violation_location, 'raw_addr') ;
  INSERT INTO raw_addresses (raw_addr_id, source_id)
  VALUES (raw_addr_token_id, raw_tickets_source_id)
  ON CONFLICT (raw_addr_id, source_id) DO UPDATE SET raw_addr_id = raw_addr_token_id
  RETURNING id into raw_addresses_id ;
  
  INSERT INTO tickets
    (ticket_number, raw_addr_id,
     time, ticket_queue, unit, badge,
     license_type, license_state, license_number, car_make, hearing_dispo)
  SELECT
    NEW.ticket_number,
    raw_addresses_id,
    to_timestamp(NEW.issue_date, 'MM/DD/YYYY HH12:MI am'),
    NEW.ticket_queue,
    NEW.unit,
    NEW.badge,
    NEW.license_type,
    NEW.license_state,
    NEW.plate_number,
    NEW.car_make,
    NEW.hearing_dispo ;
    RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION create_addr_token(new_token_str text, new_token_type text) RETURNS INT
AS $$
DECLARE token_id int ;
BEGIN
  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (new_token_str, new_token_type)
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = new_token_str
  RETURNING id into token_id ;
  RETURN token_id ;
END ;
$$ LANGUAGE plpgsql ;

CREATE TRIGGER ticket_addr_trigger AFTER INSERT ON raw_tickets
  FOR EACH ROW EXECUTE PROCEDURE raw_tickets_insert_trigger();

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
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.raw_addr
  RETURNING id into new_raw_addr_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.unit, 'unit')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.unit
  RETURNING id into new_unit_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.dir, 'direction')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.dir
  RETURNING id into new_dir_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.street_name, 'street_name')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.street_name
  RETURNING id into new_street_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.suffix, 'suffix')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.suffix
  RETURNING id into new_suffix_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.scrap, 'scrap')
  ON CONFLICT (token_str, token_type) DO UPDATE SET token_str = NEW.scrap
  RETURNING id into new_scrap_id ;

  INSERT INTO parsed_tokens (raw_addr_id, unit_id, dir_id, street_id, suffix_id, scrap_id)
  VALUES (new_raw_addr_id, new_unit_id, new_dir_id, new_street_id, new_suffix_id, new_scrap_id)
  ON CONFLICT DO NOTHING ;
  RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER parsed_tokens_trigger AFTER INSERT ON parsed_temp
  FOR EACH ROW EXECUTE PROCEDURE insert_parsed_tokens();

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
  smarty_source_id int ;

BEGIN
  SELECT id FROM data_sources
  WHERE alias = 'smartystreets'
  INTO smarty_source_id ;

  INSERT INTO addr_tokens (token_str, token_type)
  VALUES (NEW.original, 'raw_addr')
  ON CONFLICT (token_str, token_type) DO NOTHING
  RETURNING id into new_raw_addr_id ;

  INSERT INTO corrections (change_from, change_to, source)
  VALUES (NEW.original, new_raw_addr_id, smarty_source_id)
  ON CONFLICT DO NOTHING
  RETURNING id INTO new_correction_id ;

  WITH atok_updates as (
    INSERT INTO addr_tokens (token_str, token_type)
    VALUES (NEW.unit, 'unit'),
           (NEW.street_predirection, 'direction'),
           (NEW.street_name, 'street_name'),
           (NEW.suffix, 'suffix'),
           (NEW.longitude, 'longitude'),
           (NEW.latitude, 'latitude'),
           (NEW.zipcode, 'zip')
    ON CONFLICT DO NOTHING
    RETURNING id, token_str, token_type )
  INSERT INTO raw_addresses 
  (raw_addr_id, raw_unit_id, raw_direction_id, raw_street_name_id, raw_suffix_id, raw_longitude_id, raw_latitude_id, raw_zip_id, correction_id, source_id)
  VALUES (
       coalesce((SELECT id from atok_updates where token_type = 'raw_addr')
                , (SELECT at.id from addr_tokens at where token_type = 'raw_addr' and at.token_str = token_str )), 
       coalesce((SELECT id from atok_updates where token_type = 'unit')
                , (SELECT id from addr_tokens where token_str = 'unit' and at.token_str = token_str)), 
       coalesce((SELECT id from atok_updates where token_type = 'direction')
                , (SELECT id from addr_tokens where token_str = 'direction' and at.token_str = token_str)), 
       coalesce((SELECT id from atok_updates where token_type = 'street_name')
                , (SELECT id from addr_tokens where token_str = 'street_name' and at.token_str = token_str)), 
       coalesce((SELECT id from atok_updates where token_type = 'suffix')
                , (SELECT id from addr_tokens where token_str = 'suffix' and at.token_str = token_str)), 
       coalesce((SELECT id from atok_updates where token_type = 'longitude')
                , (SELECT id from addr_tokens where token_str = 'longitude' and at.token_str = token_str)), 
       coalesce((SELECT id from atok_updates where token_type = 'latitude')
                , (SELECT id from addr_tokens where token_str = 'latitude' and at.token_str = token_str)), 
       coalesce((SELECT id from atok_updates where token_type = 'zip')
                , (SELECT id from addr_tokens where token_str = 'zip' and at.token_str = token_str)), 
          new_correction_id, 
          smarty_source_id)
  ON CONFLICT DO NOTHING ;
  RETURN NULL ;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER smartystreets_trigger AFTER INSERT ON smartystreets
  FOR EACH ROW EXECUTE PROCEDURE smartystreets_post_update();
