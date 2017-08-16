#separating the required contenets based on the regular expression

#!/usr/bin/python3
import re
import concurrent.futures


#change the log file as per your location like /var/log/apache.log
log_file = './log.log'
result_dict = {}

#this is a regular expression which'll parse the log line to
#required data with name field

log_line_re = re.compile(r'''(?P<remote_host>((\d{1,3}\.){3}\d{1,3})+)\s+\S+\s+\S+\s(\[(?P<date_time>\S+)\s+\S+\])(\s*\S*){3}(?P<status>\s\d{3}\s)(?P<data>\d+)\s+(?P<web_address>("h\S+"))\s+(".*")?\s+(\*\*\d+/(?P<res_time>\d+)\*\*)(\s*\S*)''')


def parse(line):
    parsed_result = log_line_re.match(line)
    if parsed_result:
        result_dict = parsed_result.groupdict()
        if result_dict: return result_dict

def log_parse(log_file):
    with open(log_file,'r') as logs:
        with concurrent.futures.ProcessPoolExecutor() as executor:
           return executor.map(parse,logs)

if __name__ == '__main__':
    log_parse(log_file)
