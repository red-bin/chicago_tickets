BEGIN ;
COPY street_ranges (full_name, direction, street, suffix,
                  suffix_dir, min_address, max_address)
  FROM '/home/matt/data/tickets/street_ranges.csv'
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO corrections
  (field_type, change_from, change_to, mod_type)
  (SELECT 'street_name', change_from, change_to, 'levens'
   FROM levens) ;

COPY corrections (field_type, change_from, change_to, mod_type)
  FROM '/home/matt/git/chicago_tickets/data/corrections/street_type_handtyped.csv'
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

UPDATE ticket_addrs
  SET street_type = c.change_to
  FROM corrections c
  WHERE c.change_from = street_type
  AND c.field_type = 'street_type' 
  AND street_type != '' ;

UPDATE ticket_addrs
  SET street_name = c.change_to
  FROM corrections c
  WHERE c.change_from = street_name
  AND c.field_type = 'street_name'
  AND street_name != '' ;

UPDATE ticket_addrs
  SET street_type = sq.suffix
  FROM (select distinct(s1.street), s1.suffix, s1.min_address, s1.max_address
          from street_ranges s1,
          (select street, count(distinct(suffix)) as suffix_count
            from street_ranges GROUP BY street) s2
        where s1.street = s2.street 
        and s2.suffix_count = 1) sq
  WHERE sq.street = ticket_addrs.street_name
  AND ticket_addrs.street_type is NULL 
  AND ticket_addrs.street_num >= sq.min_address
  AND ticket_addrs.street_num <= sq.max_address ;

COMMIT ;
