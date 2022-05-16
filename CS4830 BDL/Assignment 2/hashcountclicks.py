#!/usr/bin/env python
import pyspark
import sys

if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <inputUri> <outputUri>")

def mapTimeBlock(timestamp):
    try:
        hour = (timestamp.split()[1].split(":")[0])
        hashmap = { 
            "00":"0-6", "01":"0-6", "02":"0-6", "03":"0-6", "04":"0-6", "05":"0-6", 
            "06":"6-12", "07":"6-12", "08":"6-12", "09":"6-12", "10":"6-12", "11":"6-12", 
            "12":"12-18", "13":"12-18", "14":"12-18", "15":"12-18", "16":"12-18", "17":"12-18", 
            "18":"18-24", "19":"18-24", "20":"18-24", "21":"18-24", "22":"18-24", "23":"18-24", 
        }        
        return hashmap[hour]
    
    except:
        return "none" 

inputUri = sys.argv[1]
outputUri = sys.argv[2]

sc = pyspark.SparkContext()
lines = sc.textFile(sys.argv[1])
words = lines.map(lambda line: mapTimeBlock(line.split(",")[0]))
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda count1, count2: count1 + count2)
wordCounts.saveAsTextFile(sys.argv[2])
