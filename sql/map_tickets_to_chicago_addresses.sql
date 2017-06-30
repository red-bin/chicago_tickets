update tickets 
set addr_id = sub_addr_id from 
  (select st.id as sub_t_id,
          sc.id as sub_addr_id 
   from tickets st, 
        chicago_addresses sc 
   where st.street_type = sc.street_type 
   and sc.street_name = st.street_name 
   and sc.street_dir = st.street_dir 
   and st.address_num=sc.address_number 
   and st.addr_id is NULL) as subquery
where id = subquery.sub_t_id 
and addr_id is NULL ;
 
