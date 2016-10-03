tickets_sql = """
CREATE TABLE tickets (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    ticket_number BIGINT,
    violation_code CHAR(15),
    address_num INTEGER,
    street_dir CHAR(10),
    street_name CHAR(30),
    street_type CHAR(10),
    time DATETIME,
    weekday INTEGER,
    ticket_queue CHAR(20),
    unit CHAR(20),
    badge CHAR(10),
    license_type CHAR(20),
    license_state CHAR(5),
    license_number CHAR(15),
    car_make CHAR(20),
    hearing_dispo CHAR(20),
    raw_location CHAR(50),
    primary key(id)
);
"""
chicago_addresses_sql= """
CREATE TABLE chicago_addresses (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    address_number INTEGER,
    street_dir CHAR(1),
    street_name CHAR(50),
    street_type CHAR(20),
    latitude FLOAT,
    longitude FLOAT,
    primary key(id)
);
"""

def populate_chicago_table(unparsed_chiaddrs):
    for unparsed in unparsed_chiaddrs:
        parsed_address,fails = addrparse.parse_address(unparsed['Address'])
        latitude = unparsed['LATITUDE']
        longitude = unparsed['LONGITUDE']

        try:
            entry = [ int(parsed_address['AddressNumber']),
                parsed_address['StreetNamePreDirectional'],
                parsed_address['StreetName'],
                parsed_address['StreetNamePostType'],
                float(latitude),
                float(longitude) ]

        except:
            try:
                entry = [ parsed_address['AddressNumber'],
                    parsed_address['StreetNamePreDirectional'],
                    parsed_address['StreetName'],
                    parsed_address['StreetNamePreType'],
                    latitude,
                    longitude ]
            except:
                entry = None

        if entry:
            chicago_addrs.append(entry)
    stmt = "INSERT INTO chicago_addresses (address_number, street_dir, street_name, street_type, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s)"
    c.executemany(stmt, chicago_addrs)
    db.commit()


