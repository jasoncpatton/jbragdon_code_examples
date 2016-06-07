# This creates a table in a PostGIS enabled PostgreSQL database called usda_districts_ia.
# It requires an existing table with Iowa counties called counties_ia.
# counties_ia must have a column geom_wgs that uses SRID 4326.

districts = {
    'Northwest': ('Lyon', 'Osceola', 'Dickinson', 'Emmet',
                  'Sioux', "O'Brien", 'Clay', 'Palo Alto',
                  'Plymouth', 'Cherokee', 'Buena Vista', 'Pocahontas'),
    'North Central': ('Kossuth', 'Winnebago', 'Worth', 'Mitchell',
                      'Hancock', 'Cerro Gordo', 'Floyd',
                      'Humboldt', 'Wright', 'Franklin', 'Butler'),
    'Northeast': ('Howard', 'Winneshiek', 'Allamakee',
                  'Chickasaw', 'Fayette', 'Clayton',
                  'Bremer', 'Black Hawk', 'Buchanan', 'Delaware', 'Dubuque'),
    'West Central': ('Woodbury', 'Ida', 'Sac', 'Calhoun',
                     'Monona', 'Crawford', 'Carroll', 'Greene',
                     'Harrison', 'Shelby', 'Audubon', 'Guthrie'),
    'Central': ('Webster', 'Hamilton', 'Hardin', 'Grundy',
                'Boone', 'Story', 'Marshall', 'Tama',
                'Dallas', 'Polk', 'Jasper', 'Poweshiek'),
    'East Central': ('Benton', 'Linn', 'Jones', 'Jackson',
                     'Iowa', 'Johnson', 'Cedar', 'Clinton',
                     'Muscatine', 'Scott'),
    'Southwest': ('Pottawattamie', 'Cass', 'Adair',
                  'Mills', 'Montgomery', 'Adams',
                  'Fremont', 'Page', 'Taylor'),
    'South Central': ('Madison', 'Warren', 'Marion',
                      'Union', 'Clarke', 'Lucas', 'Monroe',
                      'Ringgold', 'Decatur', 'Wayne', 'Appanoose'),
    'Southeast': ('Mahaska', 'Keokuk', 'Washington', 'Louisa',
                  'Wapello', 'Jefferson', 'Henry', 'Des Moines',
                  'Davis', 'Van Buren', 'Lee')
    }

# connect to the PostGIS database
import psycopg2

conn = psycopg2.connect('')
cur = conn.cursor()

# drop table (uncomment if needed)
#query = 'DROP TABLE usda_districts_ia;'
#cur.execute(query)

# create table
query = 'CREATE TABLE usda_districts_ia (name VARCHAR(13) PRIMARY KEY);'
cur.execute(query)

# create the districts
query = 'INSERT INTO usda_districts_ia (name) VALUES (%s);'
for district in districts:
    cur.execute(query, (district,))

conn.commit()

# create the geometry
query = "SELECT AddGeometryColumn('usda_districts_ia', 'geom', 4326, 'POLYGON', 2);"
cur.execute(query)

conn.commit()

# build the geometry
query = "UPDATE usda_districts_ia SET geom = c.merged FROM " +\
        "(SELECT ST_Union(geom_wgs) AS merged FROM counties_ia WHERE name IN %s) AS c " +\
        "WHERE name = %s;"
for district in districts:
    cur.execute(query, (districts[district], district))

conn.commit()
