The sequence of execution with respect to files: 

1>access_log.log
2>log_parser.py
3>complete_log_parser.py
4>main.py
5>mail.py

Work Process:
[I]	The access_log.log file is taken in log_parser.py and necessary data is extracted from it
[II]	complete_log_parser.py file computes the failed URL's, Unique IP's and Unique URL's and formats the data to be presented in mail
[III]	main.py files creates the necessary CSV files to be mailed and zippes everything up into LOGS.zip  
[IV]	mail.py sends mail with the zipped file

Changes to be made:
1)In log_parser.py change the value of log_file variable with the path of your logs file
2)In mail.py change the email_toaddrs with the receivers mail ID's separated by comma and write them in single quotes( ' ' )

What to Execute Finally?
execute: python3 mail.py

#The king never fails to win his destiny
