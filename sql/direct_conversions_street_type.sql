update tickets
set street_type = sq.change_to from
(select 
   change_from, 
   change_to 
 from corrections where mod_type = 'direct' and field_type = 'street_type' ) as sq,
(select id, street_type from tickets where addr_id = NULL)  as sq2
where tickets.street_type = sq.change_from
and tickets.addr_id is NULL
and tickets.id = sq2.id ;
