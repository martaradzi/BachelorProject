import ais
import gzip
import datetime
import os
import time
from os import listdir
from os.path import isfile, join

#####################	delimiters
split_lines = '!'
split_time = ' '
split_message = ','
split_attribute = ': '
x = "u'x'"
y = "u'y'"

#####################Limiting coordinates###########################

y0 = 61.121673
x0 = 30.349740
y1 = 58.646039
x1 = 16.634537

#####################################################################

file_counter = 0
number_of_exceptions = 0
nr_lines_r = 0
nr_lines_wr = 0

file_path_in  = "/export/scratch1/home/hannes/ais/marta/02/12/" # specifies from where the program should take files
file_path_out = "/export/scratch1/home/hannes/ais/marta/02/12/filtered/" # specifies where the processed files should be stored

# checks if a ships is withis coordinates specified beforehand
def ship_within_coordinates(observation_list):
    global y0
    global y1
    global x0
    global x1

    coordY = 0
    coordX = 0
    observations_list = observation_list.split(", ")
    for i in observations_list:
        if i.startswith(y):
            coordY = float(i.split(split_attribute)[1])
        if i.startswith(x):
            coordX = float(i.split(split_attribute)[1])
    if coordY <= y0 and coordY >= y1:
        if coordX <= x0 and coordX >= x1:
            return True
    else:
        return False


# decodes and processes a file
def decode_file(filename):
	global number_of_exceptions
    global number_of_lines
    global files_read
	global file_path_in
    global file_path_out
    global nr_lines_r
    global nr_lines_wr
    observation_list = ""
  
	file_in = file_path_in + filename
    file_out = file_path_out + filename
    with open(file_in, 'r') as f_in:
            with open(file_out, 'w') as f_out:
                for line in f_in:
                    try:
                        # lines without time stamp
                        if line.startswith(split_lines):
							#valid messages end with the value of 0
							if line.split(split_message)[6][:1] == "0":
								observation_list = str(ais.decode(line.split(split_message)[5], int(line.split(split_message)[6][:1])))
								nr_lines_r += 1
                        # lines with time stamp
                        else:
                            list1 = line.split(split_time)
                            try:
								#valid messages end with the value of 0
                                if line.split(split_message)[6][:1] == "0":
									observation_list = str(ais.decode(line.split(split_message)[5], int(line.split(split_message)[6][:1])))
									nr_lines_r += 1
							except ValueError:  # uncommon messages which start with time stamp
								number_of_exceptions += 1
								pass
                    # uncommon messages
                    except:
                        number_of_exceptions += 1
                        pass
						
                    if ship_within_coordinates(observation_list):
                        f_out.write(observation_list + "\n")
                        nr_lines_wr += 1


def read_files(mypath):
    global file_counter
    onlyfiles = [f for f in listdir(file_path_in) if isfile(join(file_path_in, f))]
	for filename in onlyfiles:
        if filename.endswith(".txt"):
            file_counter += 1
            print ("Decoding file " + str(file_counter) + ": " + filename)
            decode_file(filename)
            continue

        else:
            continue

start = time.time()

read_files(mypath)

end = time.time()

good_ships = (nr_lines_wr * 100) / nr_lines_r

print "Time elapsed: " + str(end - start)
print "Number of  read lines:  " + str(nr_lines_r)
print "Number of written lines: " + str(nr_lines_wr)
print "Percentage of ships categorized to within coordinates: " + str(good_ships) + "%"


