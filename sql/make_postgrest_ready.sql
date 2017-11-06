BEGIN ;
CREATE SCHEMA tkt AUTHORIZATION tickets ;
SET search_path TO tkt ;

CREATE VIEW tickets_view AS
  (select t.ticket_number, 
          t.time,

          v.code,
          v.description,
          v.cost,
 
          ta.raw_addr,
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
         public.addresses ta,
         public.addresses ca,
         public.violations v
        
    WHERE 
      t.addr_id = ta.id
    AND 
      t.violation_id = v.id
    AND 
      ta.id = t.addr_id);

COMMIT;
