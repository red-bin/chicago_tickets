CREATE VIEW addresses_view AS
  (SELECT 
    t_raw_addr.token_str AS raw_addr, 
    t_unit.token_str AS unit, 
    t_dir.token_str AS dir, 
    t_name.token_str AS street_name,
    t_suffix.token_str AS suffix,
    t_scraps.token_str AS scraps,
    t_longitude.token_str AS longitude,
    t_latitude.token_str AS latitude,
    a.source

    FROM 
    addr_tokens t_raw_addr,
    addr_tokens t_unit,
    addr_tokens t_dir,
    addr_tokens t_name,
    addr_tokens t_suffix,
    addr_tokens t_scraps,
    addr_tokens t_longitude,
    addr_tokens t_latitude,
    addresses a

    WHERE a.raw_addr_id = t_raw_addr.id
    AND t_unit.raw_addr_id = t_raw_addr.id
    AND t_dir.raw_addr_id = t_raw_addr.id
    AND t_name.raw_addr_id = t_raw_addr.id
    AND t_suffix.raw_addr_id = t_raw_addr.id
    AND t_scraps.raw_addr_id = t_raw_addr.id
    AND t_longitude.raw_addr_id = t_raw_addr.id
    AND t_latitude.raw_addr_id = t_raw_addr.id

    AND t_unit.token_type = 'unit'
    AND t_dir.token_type = 'dir'
    AND t_name.token_type = 'name'
    AND t_suffix.token_type = 'suffix'
    AND t_scraps.token_type = 'scraps'
    AND t_longitude.token_type = 'longitude'
    AND t_latitude.token_type = 'latitude'
);
