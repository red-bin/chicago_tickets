BEGIN ;
COPY data_sources (alias, url)
  FROM :data_sources_path
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;
COMMIT ;

BEGIN ;
COPY raw_tickets (ticket_number, plate_number, license_state, license_type, 
                  car_make, issue_date, violation_location, violation_code, 
                  violation_desc, badge, unit, ticket_queue, hearing_dispo)
  FROM :tickets_path
  WITH (FORMAT CSV, DELIMITER ';', NULL '', QUOTE '|', HEADER) ;
COMMIT ;

BEGIN ;
COPY chicago_addresses (longitude, latitude, unit, raw_addr, zip, source)
  FROM :chicago_addresses_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;
COMMIT ;

BEGIN ;
COPY street_ranges (raw_addr, direction, street, suffix,
                  suffix_dir, unit_start, unit_end)
  FROM :street_ranges_path
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

COPY levens (change_from, change_to, nleven)
  FROM :levens_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;
COMMIT ;
