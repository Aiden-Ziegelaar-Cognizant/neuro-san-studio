import duckdb
import random
import math
import datetime

con_t = duckdb.connect("tailings.db")

sites = ["Pilbara", "Gascoyne", "Murchison"]

# create sites table and populate
con_t.execute("CREATE TABLE sites (site_id INTEGER PRIMARY KEY, site_name TEXT)")
for i, site in enumerate(sites):
    con_t.execute(f"INSERT INTO sites VALUES ({i}, '{site}')")

# create 100 dataloggers with 10 char serial numbers allocatted evenly across the sites
con_t.execute("CREATE TABLE dataloggers (datalogger_id INTEGER PRIMARY KEY, site_id INTEGER, serial_number TEXT)")
for i in range(50):
    site_id = i % len(sites)
    serial_number = f"{i:010d}"
    con_t.execute(f"INSERT INTO dataloggers VALUES ({i}, {site_id}, '{serial_number}')")

# Create a specific bad datalogger with a serial number of 0000000000
con_t.execute("INSERT INTO dataloggers VALUES (1000, 0, 'BAD_DATALOGGER')")

# create 10 VWP devices per datalogger with a name that starts with VWP_ then a 5 number sequence
con_t.execute("CREATE TABLE vwp_devices (vwp_device_id INTEGER PRIMARY KEY, datalogger_id INTEGER, device_name TEXT, channel INTEGER)")
for i in range(500):
    datalogger_id = i % 50
    channel = math.floor(i / 50) + 1
    device_name = f"VWP_{i:05d}"
    con_t.execute(f"INSERT INTO vwp_devices VALUES ({i}, {datalogger_id}, '{device_name}', {channel})")

# insert 10 bad devices on the bad datalogger
for i in range(10):
    con_t.execute(f"INSERT INTO vwp_devices VALUES ({1000+i}, 1000, 'VWP_0_{i}', {i+1})")

# insert one bad device on a good data logger
con_t.execute("INSERT INTO vwp_devices VALUES (1011, 0, 'VWP_0_11', 11)")

max_level = 100

exceedence_level = 90

start_value = 50

reading_value = start_value

reading_start_date = datetime.date.today() - datetime.timedelta(days=365*5)

con_t.execute("BEGIN TRANSACTION;")

# create 5 years of daily readings per device with a value that changes between 1-5 either up or down each day
con_t.execute("CREATE TABLE readings (vwp_device_id INTEGER, reading_date DATE, reading_value INTEGER, is_exceedence BOOL, PRIMARY KEY (vwp_device_id, reading_date))")

for j in range(500):
    for i in range(365*5):
        reading_date = reading_start_date + datetime.timedelta(days=i)
        if i == 0:
            reading_value = start_value
        else:
            reading_value += random.randint(-5, 5)
        if reading_value > max_level:
            reading_value = max_level
        if reading_value < 0:
            reading_value = 0
        is_exceedence = reading_value > exceedence_level
        con_t.execute(f"INSERT INTO readings VALUES ({j}, '{reading_date.isoformat()}', {reading_value}, {is_exceedence})")

# create four and a half years of daily readings for the bad device
for i in range(365*4+180):
    reading_date = reading_start_date + datetime.timedelta(days=i)
    reading_value = 60
    is_exceedence = reading_value > exceedence_level
    con_t.execute(f"INSERT INTO readings VALUES (1011, '{reading_date.isoformat()}', {reading_value}, {is_exceedence})")

# create 4 years of daily readings for the devices on the bad data logger
for j in range(10):
    for i in range(365*4):
        reading_date = reading_start_date + datetime.timedelta(days=i)
        if i == 0:
            reading_value = start_value
        else:
            reading_value += random.randint(-5, 5)
        if reading_value > max_level:
            reading_value = max_level
        if reading_value < 0:
            reading_value = 0
        is_exceedence = reading_value > exceedence_level
        con_t.execute(f"INSERT INTO readings VALUES ({1000+j}, '{reading_date.isoformat()}', {reading_value}, {is_exceedence})")

con_t.execute("COMMIT;")

con_t.close()

con_wo = duckdb.connect("work_orders.db")

# create an inventory table with a type and quantity and location
con_wo.execute("CREATE TABLE inventory (item_id INTEGER PRIMARY KEY, item_type TEXT, quantity INTEGER, location TEXT)")

# Insert VWP and data logger rows for each site
con_wo.execute(f"INSERT INTO inventory VALUES (1, 'VWP', 5, 'Pilbara')")
con_wo.execute(f"INSERT INTO inventory VALUES (2, 'Datalogger', 0, 'Pilbara')")
con_wo.execute(f"INSERT INTO inventory VALUES (3, 'VWP', 5, 'Gascoyne')")
con_wo.execute(f"INSERT INTO inventory VALUES (4, 'Datalogger', 2, 'Gascoyne')")
con_wo.execute(f"INSERT INTO inventory VALUES (5, 'VWP', 5, 'Murchison')")
con_wo.execute(f"INSERT INTO inventory VALUES (6, 'Datalogger', 1, 'Murchison')")

con_wo.close()