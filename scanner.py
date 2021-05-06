#!/bin/python3

import sys
import socket
from datetime import datetime

#Next step defines our target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1])
	#translates hostname to ipv4
else:
	print("invalid argument value")
	print("syntax: python3 scanner.py <ip>")
	
#This next step adds a banner

print("-" * 50)
print("scanning target " + target)
print("time started: "+str(datetime.now()))
print("-" * 50)


#the actual scanning of ports 50-85
try:
	for port in range(50,85):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		result = s.connect_ex((target,port)) #returns errors
		print("Checking port {}".format(port))
		if result == 0:
			print("port {} is open".format(port))
		s.close()
	
#Handle the ability to exit/stop the program	
except KeyboardInterrupt:
	print("\nExiting program.")
	sys.exit()

except socket.gaierror:
	print("Hostname could not be resolved.")
	sys.exit()
	
except socket.error:
	print("Couldn't connect.")
	sys.exit()
