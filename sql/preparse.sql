INSERT INTO addr_tokens (token_str, token_type)
  (SELECT DISTINCT(raw_addr),'raw_addr' from addresses) ;
