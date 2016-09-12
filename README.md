# chicago_tickets

Work in progress on another attempt to clean up parking data. Currently validates ticket data and Chicago address data for simple parsing errors:
```
###Check first million tickets for errors. 

/tickets.py -t1000000 | grep Code
[('Violation Code', 'E'), ('Badge', 'EXPIRED PLATES OR TEMPORARY REGISTRATION'), ('Ticket Queue', '025')]
[('Violation Code', 'M'), ('Badge', 'EXPIRED PLATES OR TEMPORARY REGISTRATION'), ('Ticket Queue', '018')]
[('Violation Code', 'EXINGTON'), ('Badge', 'NO CITY STICKER VEHICLE UNDER/EQUAL TO 16,000 LBS.'), ('Ticket Queue', '393')]
[('Violation Code', ''), ('Badge', 'EXPIRED PLATES OR TEMPORARY REGISTRATION'), ('Ticket Queue', '004')]
[('Violation Code', 'LARK'), ('Badge', 'OBSTRUCT ROADWAY'), ('Ticket Queue', '020')]
[('Violation Code', ''), ('Badge', 'EXP. METER NON-CENTRAL BUSINESS DISTRICT'), ('Ticket Queue', '002')]
[('Violation Code', 'PMG'), ('Badge', 'STREET CLEANING'), ('Ticket Queue', '498')]
[('Violation Code', ''), ('Badge', 'DOUBLE PARKING OR STANDING'), ('Ticket Queue', '002')]
[('Violation Code', ''), ('Badge', 'EXPIRED PLATES OR TEMPORARY REGISTRATION'), ('Ticket Queue', '009')]
[('Violation Code', ''), ('Badge', 'STREET CLEANING'), ('Ticket Queue', '006')]
[('Violation Code', ''), ('Badge', '0964080B'), ('Unit', 'NO STANDING/PARKING TIME RESTRICTED'), ('Ticket Queue', '11378')]
[('License Plate Number', ''), ('Violation Code', 'D'), ('Badge', 'EXPIRED PLATES OR TEMPORARY REGISTRATION'), ('Ticket Queue', '018')]
```
