#!/usr/bin/env python3
import os, csv, re
from collections import OrderedDict
expr= r'''(?P<k1>(.*))[,](?P<v1>(.*))'''    
result={}

#Give CSV files location and check if they exists
csvfiles=["1.csv","2.csv"]
if not os.path.isfile(csvfiles[0]):
  print("file "+ csvfiles[0] + " doesn't exists" )
  exit()
if not os.path.isfile(csvfiles[1]):
  print("file "+ csvfiles[1] + " doesn't exists" )
  exit()

#from CSV files write it to dictionary and eliminate entries with value "" " " and "\n"
for csvFile in csvfiles:
	with open(csvFile, "r") as matching:
	    for line in matching:
	        line = line.strip()
	        if re.match(expr, line):
	           (key, val) = line.split(',')
	           if val==" " or val=="" or val=="\n":
	            continue
	           if key in result:
	              result[key]=int(result[key])+int(val)
	           else:
	              if key.strip():
	                result[key] = int(val.rstrip('\n'))
	                result[key]=val

#sort the values in descending order with more number of commits at the top
result = OrderedDict(sorted(result.items(), key=lambda v: v[1], reverse=True))

with open("./COMMIT_DETAILS.csv","w") as wr:
  writecsv=csv.writer(wr)
  writecsv.writerow(["NAME","TOTAL COMMITS"])
  writecsv.writerow(["",""])#Add empty line for indentation
  for k in result:
      writecsv.writerow([k,result[k]])
