INSERT INTO corrections
  (change_from, change_to, token_type_id, mod_type)
  (SELECT change_from, change_to, tt.id, 'levens'
   FROM levens l, token_types tt
   WHERE tt.token_type = 'suffix');

COPY corrections (token_type_id, change_from, change_to, mod_type)
  FROM '/home/matt/git/chicago_tickets/data/corrections/street_type_handtyped.csv'
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

UPDATE addresses
  SET street_type = c.change_to
  FROM corrections c, token_types tt 
  WHERE c.change_from = street_type
  AND tt.token_type = 'suffix' 
  AND corrections.token_type_id = tt.id
  AND street_type != '' ;

UPDATE addresses
  SET street_type = c.change_to
  FROM corrections c, token_types tt 
  WHERE c.change_from = street_type
  AND tt.token_type = 'name' 
  AND corrections.token_type_id = tt.id
  AND street_type != '' ;

--UPDATE addresses
  --SET street_type = sq.suffix
  --FROM (SELECT distinct(s1.street), s1.suffix, s1.min_address, s1.max_address
          --FROM street_ranges s1,
          --(SELECT street, count(distinct(suffix)) AS suffix_count
            --FROM street_ranges GROUP BY street) s2
            --WHERE s1.street = s2.street 
          --AND s2.suffix_count = 1) sq,
          --data_sources ds

  --WHERE sq.street = addresses.street_name
  --AND addresses.street_type IS NULL 
  --AND addresses.street_num >= sq.min_address
  --AND addresses.street_num <= sq.max_address ;
  --AND addresses.data_source = ds.id
  --AND ds.alias in ('tickets', 'openaddr')
