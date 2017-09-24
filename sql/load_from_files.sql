BEGIN ;

CREATE TEMPORARY TABLE raw_tickets (
  id SERIAL PRIMARY KEY,
  ticket_number BIGINT,
  plate_number TEXT,
  license_state TEXT,
  license_type TEXT,
  car_make TEXT,
  issue_date TEXT,
  violation_location TEXT,
  violation_code TEXT,
  violation_desc TEXT,
  badge TEXT,
  unit TEXT,
  ticket_queue TEXT,
  hearing_dispo TEXT) ;

COPY raw_tickets (ticket_number, plate_number, license_state, license_type, 
                  car_make, issue_date, violation_location, violation_code, 
                  violation_desc, badge, unit, ticket_queue, hearing_dispo)
  FROM '/home/matt/data/tickets/tickets.csv' 
  WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER) ;

INSERT INTO violations (code, description, cost)
  SELECT violation_code, violation_desc, 0
   FROM raw_tickets
   GROUP BY violation_code, violation_desc ;

INSERT INTO ticket_addrs (addrstr_raw, street_num, street_dir)
  SELECT violation_location,
       CASE WHEN split_part(violation_location, ' ', 1) ~ '^[0-9]+$' 
          THEN split_part(violation_location, ' ', 1)::integer 
          ELSE -1
       END,
       CASE WHEN split_part(violation_location, ' ', 2) ~ '^[NESWnesw]$'
          THEN split_part(violation_location, ' ', 2)
          ELSE ''
       END
     FROM raw_tickets
     GROUP BY violation_location ;

UPDATE ticket_addrs
  SET addrstr_current = regexp_replace(addrstr_raw, '^[^ ]+ [^ ]+ ', '') 
  WHERE street_dir in ('N','E','S','W') AND street_num IS NOT NULL ;

UPDATE ticket_addrs
  SET addrstr_current = regexp_replace(addrstr_raw, '^[^ ]+ ', '') 
  WHERE street_dir not in ('N','E','S','W') and street_num it not NULL ;

INSERT INTO tickets (ticket_number, violation_id,
                     addr_id, time, ticket_queue, unit, 
                     badge, license_type, license_state, 
                     license_number, car_make, hearing_dispo)
  SELECT 
    r.ticket_number,
    v.id,
    a.id,
    to_timestamp(r.issue_date, 'MM/DD/YYYY HH12:MI am'),
    r.ticket_queue,
    r.unit,
    r.badge,
    r.license_type,
    r.license_state,
    r.plate_number,
    r.car_make,
    r.hearing_dispo
  FROM 
    raw_tickets r,
    ticket_addrs a, 
    violations v
  WHERE 
    r.violation_location = a.addrstr_raw
    and v.code = r.violation_code 
    and v.description = r.violation_desc ;

COMMIT ;
