# This creates a table called temp_smos_iowa
# containing SMOS pixel geometries
# based on a list of DGGs.

# select the DGGs
dggs = [194406, 197495, 200052, 202112, 203632, 200057]

# connect to the database
import psycopg2

conn = psycopg2.connect('')
cur = conn.cursor()

# drop the table (uncomment if needed)
#query = 'DROP TABLE temp_smos_iowa'
#cur.execute(query)

# create the table
query = 'CREATE TABLE temp_smos_iowa (dgg INT PRIMARY KEY)'
cur.execute(query)

# insert DGGs into the table
query = 'INSERT INTO temp_smos_iowa (dgg) VALUES (%s)'
for dgg in dggs:
    cur.execute(query, (dgg,))

conn.commit()

# create the geometry
query = "SELECT AddGeometryColumn('temp_smos_iowa', 'geom', 4326, 'POLYGON', 2)"
cur.execute(query)

conn.commit()

# copy the pixel geometries from smos_grid_ia
query = '''
UPDATE temp_smos_iowa SET geom = ST_Transform(s.geom_43km, 4326) 
FROM (SELECT geom_43km FROM smos_grid_ia WHERE dgg = %s) AS s 
WHERE dgg = %s
'''
for dgg in dggs:
    cur.execute(query, (dgg, dgg))

conn.commit()
