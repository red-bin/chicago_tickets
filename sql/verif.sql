select t.street_name, count(t.street_name) 
from tickets t 
where t.street_name not in 
  (select distinct(street) 
   from street_ranges)
group by t.street_name 
order by count(t.street_name) desc ;
