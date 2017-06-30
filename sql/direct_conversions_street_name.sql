update tickets
set street_name = sq.change_to from
(select 
   change_from, 
   change_to 
 from corrections where mod_type = 'direct' and field_type = 'street_name' ) as sq,
(select id, street_name from tickets)  as sq2
where tickets.street_name = sq.change_from
and tickets.id = sq2.id ;
