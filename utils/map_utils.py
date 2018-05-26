SELECT sum(cost), time_bucket('1 day', issue_date), neighborhood
   FROM violations as v, addresses AS a
  INNER JOIN tickets AS t
  ON t.violation_location = a.original
  WHERE v.code = t.violation_code
  GROUP BY time_bucket('1 day', issue_date), neighborhood;
