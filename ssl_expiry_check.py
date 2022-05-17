#!/usr/bin/python3

import schedule
import time
import datetime
import socket
import ssl
import smtplib 

def get_num_days_before_expired(hostname: str, port: str = '443') -> int:
	try: 
	    #Create your SMTP session 
	    smtp = smtplib.SMTP('smtp.gmail.com', 587) 
	
	   #Use TLS to add security 
	    smtp.starttls() 
	
	    #User Authentication 
	    smtp.login("domadiyaamish@gmail.com","password")
	
	    #Defining The Message 
	    message = "this domain ssl certificate expiry soon" 
	    messagetosend = hostname+message
	    context = ssl.create_default_context()
	    with socket.create_connection((hostname, port)) as sock:
	        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
	            ssl_info = ssock.getpeercert()
	            expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
	            delta = expiry_date - datetime.datetime.utcnow()
	            print(f'{hostname} expires in {delta.days} day(s)')
	            if( delta.days <=7):
	            	#Sending the Email
	            	smtp.sendmail("domadiyaamish@gmail.com", "amishdomadiya2158@gmail.com",messagetosend) 			    
	            	#Terminating the session 
	            	smtp.quit() 
	            	print ("Email sent successfully!") 
	            return delta.days
	except Exception as ex: 
		    print("Something went wrong....",ex)


            
def do_nothing():
	domain =[]
	my_file = open("live_subdomains.txt", "r")
	data = my_file.read()
	data_into_list = data.split("\n")
	domain.append(data_into_list)
	n=len(data_into_list)
	print(n)
	print(domain)
	my_file.close()
	domains = data_into_list
	for i in domains:
		get_num_days_before_expired(i)
	
	

schedule.every(1).day.do(do_nothing)

while True:
     schedule.run_pending()
     time.sleep(1)

