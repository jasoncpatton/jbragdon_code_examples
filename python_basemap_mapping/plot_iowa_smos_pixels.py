### Decouple matplotlib from X
import matplotlib
matplotlib.use('agg')

## Locations

smos_points = [(-96.15, 43.065), (-93.44, 43.08),
               (-94.65, 42.263), (-92.15, 42.05),
               (-95.36, 41.11)]

coops = {
    'Sheldon': (-95.9, 43.2),
    'IA NC Climate Division': (-93.5, 43.0),
    'Fort Dodge': (-94.2, 42.5),
    'Waterloo': (-92.4, 42.6),
    'IA SW Climate Division': (-95.1, 41.1)
    }

iems = {
    'Sutherland/Calumet': (-95.5, 42.9),
    'Kanawha': (-93.8, 42.9),
    'Gilbert': (-93.6, 42.1),
    'Lewis': (-95.2, 41.3)
    }

## Map 

# Iowa bounds ('c' at center of state)
lats = {'n':  43.5, 's':  40.35, 'c':  42.0}
lons = {'e': -90.1, 'w': -96.65, 'c': -93.4}

buf = 0.05 # plot buffer size [deg]

res = 'c' # map shapes resolution

# Projection parameters
proj = 'cea' # cylindrical equal area
lat_ts = lats['c'] # true scale at geographic center

## Create the map
from mpl_toolkits.basemap import Basemap
m = Basemap(projection = proj, lat_ts = lat_ts, resolution = res,
            urcrnrlon = lons['e'] + buf, urcrnrlat = lats['n'] + buf,
            llcrnrlon = lons['w'] - buf, llcrnrlat = lats['s'] - buf,
            fix_aspect = False)

## Plots

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np

# set width, height, and DPI
(w, h) = (6.5, 4.5)
dpi = 150

# Create the figure
fig = plt.figure(1, (w, h), dpi=dpi)
ax = fig.add_axes([0, 0, 1, 1])

# Read shapefiles (note that only the line properties can be set here)
# use drawbounds=True for shapefiles that should be plotted directly (counties and districts)
m.readshapefile('shapefiles/counties_ia', 'county', drawbounds=True,
                linewidth=0.5, color='0.8',
                zorder=1)

m.readshapefile('shapefiles/usda_districts_ia', 'usda_districts', drawbounds=True,
                linewidth=2,
                zorder=3)

m.readshapefile('shapefiles/smos_pixels', 'smos_pixels', drawbounds=False)

# create a PatchCollection from the SMOS pixels so we can fill them
patches = []
for info, shape in zip(m.smos_pixels_info, m.smos_pixels):
    patches.append(Polygon(np.array(shape), True))
    
pc = PatchCollection(patches, facecolor='0.5', linewidth=0, zorder=2)
ax.add_collection(pc) # *now* add the SMOS pixels to the map

# Initialize the map
m.drawmapboundary(linewidth=0)

# plot the NWS COOP stations
for coop in coops:
    (x,y) = m(*coops[coop])
    s1 = ax.scatter(x, y, marker='^', c='g', s=50, zorder=4)

# plot the IEM stations
for iem in iems:
    (x,y) = m(*iems[iem])
    s2 = ax.scatter(x, y, marker='s', c='b', s=50, zorder=4)

# plot the SMOS point numbers
for i,smos in enumerate(smos_points):
    (x,y) = m(*smos)
    ax.text(x, y, '%d' % (i+1), zorder=5,
            size=20, family='sans-serif', ha='center', va='center')

# add a legend for the different station types
ax.legend([s1, s2], ['NWS COOP', 'IEM'], fontsize=14, loc=4)
    
# Save the map
fig.savefig('iowa_smos_map.pdf', dpi=dpi)

