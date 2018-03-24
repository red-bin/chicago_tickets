BEGIN ;

\set parsed_addresses_path '\'' :datadir 'parsed_addresses.csv\''

COPY parsed_temp (raw_addr, unit, dir,
                  street_name, suffix, scrap)
  FROM :parsed_addresses_path
    WITH (FORMAT CSV, DELIMITER ',', NULL '') ;

COMMIT ;
