BEGIN ;
CREATE SCHEMA tkt AUTHORIZATION tickets ;
SET search_path TO tkt ;

CREATE VIEW tickets_view AS
  (select t.ticket_number, 
          t.time,

          v.code,
          v.description,
          v.cost,
 
          ta.addrstr_raw,
          ta.street_num,
          ta.street_dir,
          ta.street_name,
          ta.street_type,

          ca.latitude,
          ca.longitude,
          
          t.license_type,
          t.license_state,
   
          t.unit,
          t.badge
  
    FROM public.tickets t,
         public.ticket_addrs ta,
         public.chicago_addrs ca,
         public.violations v
        
    WHERE 
      t.addr_id = ta.id
    AND 
      t.violation_id = v.id
    AND 
      ta.id = t.addr_id);

COMMIT;
