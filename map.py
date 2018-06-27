from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('tkagg')
import numpy as np
import time
import sys
import os

y0 = 66
x0 = 33
y1 = 55
x1 = 15

def fill_array(line):
    global lons
    global lats
    sub = line.split(", ")
    for ig in sub:
        if ig.startswith("u'y'"):
            coordY = float(ig.split(": ")[1])
	    lats.append(coordY)
            #print coordY
	    
        elif ig.startswith("u'x'"):
            coordX = float(ig.split(": ")[1])
	    lons.append(coordX)
            #print coordX
 
 
 
start = time.time()
lons = []
lats = []
file_counter = 0

for filename in os.listdir(os.getcwd()):
    file_counter = file_counter + 1
    print file_counter
    if filename.endswith("00.txt") or filename.endswith("30.txt"):
        with open(filename, "r") as f_in:
            print filename
            for line in f_in:
	        fill_array(line)
map = Basemap(projection='merc', lat_0 = 59.311560, lon_0 = 20.508763, area_thresh = 1, llcrnrlon=x1, llcrnrlat=y1, urcrnrlon=x0, urcrnrlat=y0, resolution = 'i')
map.drawcoastlines()
map.drawcountries()


remove_this = 0
for lon, lat in zip(lons, lats):
    remove_this = remove_this +1
    x, y = map.projtran(lon, lat)        # coord transformationi

    map.plot(x, y, 'bo', markersize=1)  # needs grid coords to plot
    if remove_this &100 == 0:
        print remove_this



plt.show()
end = time.time()

print("Time elapsed: " + str(end - start))
