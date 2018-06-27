import sys
import os
import time

path = "/export/scratch1/home/hannes/ais/marta/speed/square/" # specifies where the processed files should be stored

start = time.time()

file_counter = 0
for filename in os.listdir(os.getcwd()):
	file_counter = file_counter + 1
	if filename.endswith(".txt"):
		print ("reading " + filename)
		f_in = open(filename, "r")
                sub = filename.split("_")
	        day = sub[0]
	        x = sub[1]
	        y = sub[2]
	        name = path + x + "_" +y
	        with open(name, "a") as f_out:
		    for line in f_in:
			f_out.write(day + ","+ line+ "\n")
		continue
	else:
		continue

end = time.time()
print("Time elapsed: " + str(end - start))
print file_counter
