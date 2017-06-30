update tickets 
set violation_id = sub_viol_id from 
  (select 
       st.id as sub_t_id,
       sv.id as sub_viol_id 
     from tickets st, 
          violations sv 
   where st.violation_code = sv.code) as subquery
where id = subquery.sub_t_id ;
