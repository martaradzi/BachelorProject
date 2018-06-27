###################################################################################################
#                                                                                                  # 
#                     Improved implementation using Apache Spark                                   #
#                                                                                                  #
####################################################################################################

from pyspark import SparkContext
from pyspark.sql import SparkSession
sc = SparkContext("local[*]", "ais")

import sys
import ais
import os
import re
import time
import math
import csv
from pyspark.sql import Row

####################################################################################################

# check for invalid values, round timestamp to closest minute, return only [time, y, x, mmsi]
def filter(line):
    x = 0
    y = 0
    time = 0
    sog = 0
    filtered_message = [0, 0, 0, 0]

    if line == 'empty':
        return filtered_message

    observation_list = line.split(", ")
    for i in observation_list:
        if i.startswith("u'timestamp'"):
            timestamp = i.split(": ")
            time = int(re.sub("[^0-9]", "", timestamp[1]))
            if time > 1:
                time = time // 10 ** (int(math.log(time, 10)) -9)
                time -= time % 60
            else:
                return filtered_message
		if i.startswith("u'sog'"):
            sog1 = i.split(": ")
            sog  = sog1[1]
        if i.startswith("u'y'"):
            y_coordinate = i.split(": ")
            y = float(y_coordinate[1])
        if i.startswith("u'x'"):
            x_coordinate = i.split(": ")
            x = float(x_coordinate[1])
	filtered_message =  [time, sog, y, x]
    return filtered_message

# decode one message
def decode_line(line, timestamp):
    decoded = 'empty'

    try:
        line_list = line.split(",")
        field_0 = line_list[0]

        if(field_0[0] != "!"):
                # timestamp is present
                timestamp = field_0[:17]

        # the message to be decoded is in the 5th field of the list
        # field 6 contains information on the type; types starting with 0 can be successfuly decoded
        field_6 = line_list[6].rstrip('\r\n')

        if (str(field_6)[0] == "0"):
            decoded_without_timestamp = str((ais.decode(str(line_list[5]), 0)))
            ## insert current timestamp value
            timestamp_position = (decoded_without_timestamp).find("timestamp") + 12
            decoded = decoded_without_timestamp[:timestamp_position] + (timestamp) + decoded_without_timestamp[timestamp_position+3:]
        else:
            pass
            # message type invalid
    except Exception:
        pass
    return decoded, timestamp


# loop through lines of a partition and decode
def decode_loop(lines):
    decoded = []
    timestamp = 0
    for line in lines:
        line, timestamp = decode_line(line, timestamp)
        decoded.append(line)
    return decoded


###################################################################################################
#                                       main                                                      # 
###################################################################################################

start_time = time.time()

# read in all .txt files in current directory
inputRDD = sc.textFile("/export/scratch1/home/hannes/ais/marta/02/11/*.txt")
input_size = inputRDD.count()

# new RDD with decoded ais messages
decodedRDD = inputRDD.mapPartitions(lambda partition: decode_loop(partition))

filteredRDD = decodedRDD.map(lambda line: filter(line)) \
        .filter(lambda line: 'empty' not in line)

spark = SparkSession(sc)
hasattr(filteredRDD, "toDF")

df = filteredRDD.toDF(['time', 'sog', 'y', 'x'])

df = df.filter(df.time != '0').filter(df.y <= 61.121673).filter(df.y >= 58.646039).filter(df.x <= 30.349740).filter(df.x >= 16.634539) 
after_duplicate_removal = df.count()

df.printSchema()
df.show()

end_time = time.time()
print("Read messages: " + str(input_size))

print after_duplicate_removal
print("Time elapsed: " + str(end_time - start_time))
print decodedRDD.take(2)
df.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("mydata.csv")
