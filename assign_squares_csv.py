import datetime
import os
import time
from os import listdir
from os.path import isfile, join
import csv

#####################	delimiters

split_atribute = ": "
split_message = ", "
sog = "u'sog'"

output_filepath = "/export/scratch1/home/hannes/ais/marta/speed/02/02/" # specifies where the processed files should be stored

#####################Limiting coordinates###########################
y0 = 61.121673
x0 = 30.349740
y1 = 58.646039
x1 = 16.634537
#####################################################################

#assigns ship to a coordinate
def classify_position(time, speed, coordX, coordY):

    global lat_difference
    global long_difference
    global x
    global y
    global output_filepath

    distanceX = coordX - x1
    distanceY = y0 - coordY

    numberX = int(distanceX/x)
    numberY = int(distanceY/y)

    date = time.split()
    hour1 = date[1]
    hour = hour1[:2]

    filepath_out = output_filepath + hour + "_" + str(numberX) + "_" + str(numberY) + ".txt"

    with open (filepath_out, "a") as f_out:
        f_out.write(speed + "\n")




		
lat_difference = 30.349740 - 16.634537
long_difference = 61.121673 - 58.646039

x = lat_difference/40
y = long_difference/10

start = time.time()

for filename in os.listdir(os.getcwd()):
    f_count += 1
    if filename.endswith(".csv"):
		with open('filename', "rb") as f_in:
			csv_f_in = csv.reader(f_in)
			for row in csv_f_in:
				time = str(datetime.datetime.fromtimestamp(float(row[0])))
				speed = float(row[1])
				coordY = float(row[2])
				coordX = float(row[3])
				classify_position(time, speed, coordX, coordY)
				continue
		
end = time.time()
print "Time elapsed: " + str(end - start)
