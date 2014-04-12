#!/usr/bin/python
#send email file program
import sys, os
from custompy.custom_utilities import parse_kwargs

def send_email_file(subject,namepath,**kwargs):
	recipient = parse_kwargs('to','chiquete.carlos@gmail.com',**kwargs)
	emailcmd='thunderbird -compose to="'+recipient+'",subject="'+subject+ \
		'",body="autosent",attachment="file://'+os.path.realpath(namepath)+'"' 
	failure = os.system(emailcmd)
	print "File path : ", namepath
	
if __name__ == "__main__":
	print "Sending email with file. "
	N = len(sys.argv)
	change_recipient = False
	print sys.argv
	recipient = "'"
	for i in range(N):
		if (i >= 1):
			if (sys.argv[i]=='-f'): 
				subject = 'EMAILED_FILE : '+sys.argv[i+1]
				file1   = sys.argv[i+1]
			if (sys.argv[i]=='-to'):
				if ( change_recipient == False): recipient = recipient+sys.argv[i+1]
				else: recipient = recipient+","+sys.argv[i+1]
				change_recipient = True
	recipient = recipient+"'"
	print recipient
	if (change_recipient == False):send_email_file(subject,file1)
	else: send_email_file(subject,file1,to=recipient)
