import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os
import time
from os import listdir
from os.path import isfile, join

file_counter = 0

path_out = "/export/scratch1/home/hannes/ais/marta/speed/calc/" # specifies where the processed files should be stored
day = "" 
	
	
def read_files():
	
	global file_counter
    global day
	
	for filename in os.listdir(os.getcwd()):
	    file_counter += 1
	    if filename.endswith(".txt"):
			print ("Reading file " + str(file_counter) +": " + filename )
			speed_array = []	
	########################make array of all the speeds############
			file_in = open(filename, "r")
			f_out_name = path_out + filename
			
			for line in file_in:
                if len(line.strip()) == 0 :
                    continue
                elif "L" not in line:
                    if float(line) != 0:	# can be commented out to include speed values of 0
                        speed_array.append(float(line))
					else:
                        new_str = line.replace("L", "")
                        if float(new_str) != 0: # can be commented out to include speed values of 0
                            speed_array.append(float(new_str))
		

			if len(speed_array)> 0: 
                a = np.array(speed_array)
				np_array = np.sort(a)
                mean = np.mean(np_array)
				std_dev = np.std(np_array)
				mode = stats.mode(np_array)
	            median = np.median(np_array) ####(Q2)
	    	    q75, q25 = np.percentile((np_array), [75,25])

				f_out = open(f_out_name, "a")
				f_out.write(str(mean) + "," + str(std_dev) + "," + str(mode[0]) + "," + str(q25) + "," + str(median) + "," + str(q75))
	

start = time.time()
read_files()

end = time.time()

t = end - start
print "time: " + str(t)
print "number of files read: " + str(file_counter)

