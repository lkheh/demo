#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 2:
	print "Usage: vrfy.py <username>"
	sys.exit(0)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a Socket
connect=s.connect(('10.11.1.217',25)) # Connect to the Server

banner=s.recv(1024)		    # Receive the banner
print banner

s.send('VRFY ' +sys.argv[1] + '\r\n') #VRFY a user
result=s.recv(1024)
print result

#Close the socket
s.close()	
