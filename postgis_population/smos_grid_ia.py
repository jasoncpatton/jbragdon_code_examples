# This creates a table in a PostGIS enabled PostgreSQL database
# with SMOS points and (circular) pixels.

# table name
table = 'smos_grid_ia'

# set bounds for Iowa
ia = {
    'n':  44.0, 's':  40.0,
    'e': -90.0, 'w': -97.0,
}

# connect to the database
import psycopg2

conn = psycopg2.connect('')
cur = conn.cursor()

# drop the table (uncomment if needed)
#query = 'DROP TABLE %s' % (table)
#cur.execute(query)

# create the table
query = '''
CREATE TABLE %s (
dgg INT PRIMARY KEY, 
longitude DOUBLE PRECISION, 
latitude DOUBLE PRECISION)
''' % (table)
cur.execute(query)

# loop through isea4h9 grid and store the pixels inside the bounds
for line in open('isea4h9.txt'):
    col = line.split()

    # get the DGG, longitude, and latitude
    dgg = int(col[0])
    lon = float(col[1])
    lat = float(col[2])

    # skip points outside of the bounds
    if not ((lat > ia['s'] and lat < ia['n']) and
            (lon > ia['w'] and lon < ia['e'])): continue

    # store points inside bounds
    query = 'INSERT INTO ' + table + ' (dgg, longitude, latitude) VALUES (%s, %s, %s)'
    cur.execute(query, (dgg, lon, lat))

conn.commit()

# create the point geometry
query = "SELECT AddGeometryColumn('%s', 'geom', 4326, 'POINT', 2)" % (table)
cur.execute(query)

query = 'UPDATE %s SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)' % (table)
cur.execute(query)

conn.commit()

# create the pixel geometry (use UTM zone 15N, SRID 26915)
query = "SELECT AddGeometryColumn('%s', 'geom_43km', 4326, 'POLYGON', 2)" % (table)
cur.execute(query)

radius = 43000./2 # 43 km diameter
query = '''
UPDATE %s 
SET geom_43km = ST_Transform(ST_Buffer(ST_Transform(geom, 26915), %f), 4326)
''' % (table, radius)
cur.execute(query)

conn.commit()
