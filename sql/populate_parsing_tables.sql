COPY street_ranges (full_name, direction, street, suffix,
                  suffix_dir, min_address, max_address)
  FROM '/home/matt/data/tickets/street_ranges.csv'
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO corrections 
  (field_type, change_from, change_to, mod_type) 
  (SELECT 'street_name', change_from, change_to, "nleven" 
   FROM levens) ;
