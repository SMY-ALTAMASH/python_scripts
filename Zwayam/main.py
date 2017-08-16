import csv
import os
import shutil
from complete_log_parser import Url, ip, fail, URl

#create a directory if not exists for storing CSV files called CSV
if not os.path.exists("CSV"):
    os.makedirs("CSV")

#generating CSV files
with open("ip.txt", "a") as f:
	f.write(str(ip))

in_txt2 = csv.reader(open("ip.txt", "r"), delimiter=' ')
with open("./CSV/UNIQUE_IP.csv", 'w') as out_csv2:
	out = csv.writer(out_csv2)
	out.writerows(in_txt2)

with open("url.txt", "a") as f:
	f.write(str(Url))

in_txt3 = csv.reader(open("url.txt", "r"), delimiter=' ')
with open("./CSV/URL.csv", 'w') as out_csv3:
	out = csv.writer(out_csv3)
	out.writerows(in_txt3)

with open("./CSV/FAILED_URL_404.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["FAILED_URL","NO_OF_TIMES_FAILED"])
    writer.writerow(["",""])
    for key, value in URl.items():
       writer.writerow([key, value])

#removing unwanted and cached files
os.remove("url.txt")
os.remove("ip.txt")
cmd = "rm -r __pycache__"
os.system(cmd)

#creating a zip in same folder for mailing
shutil.make_archive("LOGS", 'zip', "CSV")

print("Hurray")
