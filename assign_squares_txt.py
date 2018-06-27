import ais
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


output_filepath = "/export/scratch1/home/hannes/ais/marta/speed/02/01/"  # specifies where the processed files should be stored
day = output_filepath[48:50]

#####################Limiting coordinates###########################

y0 = 61.121673 
x0 = 30.349740 
y1 = 58.646039 
x1 = 16.634537

#####################Limiting coordinates###########################

no_r_rows = 0
no_wr_rows = 0
no_0 = 0


#extracts features from a list of feature
def get_features(row, filename):
    time = ""
    speed = ""
    coordX = 0
    coordY = 0

    for i in row:
        if i.startswith("u'y'"):
            coordY  = float(i.split(": ")[1])
        elif i.startswith("u'x'"):
            coordX = float(i.split(": ")[1])
        elif i.startswith("u'sog'"):
            speed = i.split(": ")[1]
    classify_position(speed, coordX, coordY, filename)


	
#assign square based on position 
def classify_position(str_speed, coordX, coordY, filename):
    global lat_difference
    global long_difference
    global x
    global y
    global output_filepath
    global no_wr_rows
    global day
    global no_0
                               
    distanceX = coordX - x1
    distanceY = y0 - coordY
                                        
    numberX = int(distanceX/x)
    numberY = int(distanceY/y)

    i if "L" not in str_speed:
        speed = str_speed
    else:
        new_str = str_speed.replace("L", "")
        speed = new_str

   # hour = filename[:2]
    if speed != "0":
        filepath_out = output_filepath + day + "_"+ str(numberX) +"_" + str(numberY) + ".txt"
        with open (filepath_out, "a") as f_out:
            f_out.write(speed + "\n")
            no_wr_rows += 1
        #print "Number of rows written: " + str(no_wr_rows)
    else:
        no_0 += 1

 


lat_difference = 30.349740 - 16.634537
long_difference = 61.121673 - 58.646039

x = lat_difference/40
y = long_difference/10

start = time.time()
f_count = 0
for filename in os.listdir(os.getcwd()):
    f_count += 1
    if filename.endswith(".txt"):
        file1 = open(filename, "r")
        for line in file1:
            row = line.split(", ")
            get_features(row, filename)
            no_r_rows += 1
            continue

end = time.time()
print "time: "
print end-start
print "no of files: " + str(f_count)
print "no of rows: " + str(no_r_rows)
print "no of zeros: " + str(no_0)


