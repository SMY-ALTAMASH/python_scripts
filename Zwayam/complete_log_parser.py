#customizing and formatting the output of mail body and csv files

#!/usr/bin/env python3

import os
import sys
from log_parser import log_parse as parse
import re
from log_parser import log_file

#variable declaration
ips = {}
status = {}
page_time = {}
count = 1
max_wait_time = 0
min_wait_time = 999999999

#checking for log file
if not os.path.isfile(log_file):
    print("please enter a valid file in script. eg: /var/log/apache.log!!!")
    sys.exit(1)

#create a custom list for holding start and end time(list that'll store only 2 values)
class customList(list):
    def append(self, val):
        if len(self) >= 2:
            self[1] = val
        else:
            list.append(self, val)

expr="^ 4.. "
#aURL={} #contains all the URL's
URl={} #contains failed URL's
var=0
fail=""

#parsing log
date_time = customList()

parsed_log = parse(log_file)
for result in parsed_log:
    if result:
        if result['date_time']:
            date_time.append(result['date_time'])

        if result['remote_host'] in ips:
            ips[result['remote_host']] +=1
        else:
            ips[result['remote_host']] = 1

        if int(result['res_time']) > max_wait_time:
            max_wait_time = int(result['res_time'])
        elif int(result['res_time']) < min_wait_time and int(result['res_time']) > 0:
            min_wait_time = int(result['res_time'])

        if result['web_address'] in page_time:
            count += 1
            page_time[result['web_address']] += int(result['res_time'])
            # aURL.update({result['web_address']:page_time[result['web_address']]})
        else:
            page_time[result['web_address']] = int(result['res_time'])
            # aURL.update({result['web_address']:page_time[result['web_address']]})
    
        if result['status'] in status:
            status[result['status']] += 1
        else:
            status[result['status']] = 1

        if re.search(expr,result['status']) and result['web_address'] in URl:
            fail=fail+"\n"+result['web_address']
            var=var+1
            URl.update({result['web_address']:var})
        else:
            var=1
            URl.update({result['web_address']:var})



no_of_requests= sum(1 for line in open(log_file))
max_wait_time /=1000
min_wait_time /=1000
average_wait_time =(max_wait_time+min_wait_time)/no_of_requests*1000

#creating mail body
other = """LOG REPORT:
\"From   {}   to    {}\"\n""".format(date_time[0],date_time[1])
ip="""UNIQUE_IP COUNT
	\n"""\
+"\n".join("{} {}".format(k,v) for k,v in ips.items())
misc ="""\n\nRESPONSE_TIME		 			 (M SEC)\n
ALL_REQUESTS				  	  {}
MAXIMUM 						{}
MINIMUM							 {}
AVERAGE 						{}\n\n""".format(no_of_requests,max_wait_time,min_wait_time,average_wait_time)
resp = """ RESPONSE_CODE   			   COUNT\n\n"""\
+"\n".join("{}								{}".format(k,v)for k,v in status.items())

Url = """URL \"TOP AVERAGE WAITING TIME(M SEC)\"        
		\n"""\
+"\n".join("{} {:.4}".format(k,v/(count*1000))for k,v in sorted(page_time.items(),key=lambda x: x[1],reverse = True))


#body of the mail
body = other + misc + resp + ".\n\nThe below attachment contains URL's visited, unique IP's and the URL's with file not found error"
