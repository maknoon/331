"""
Programming Assignment #4: Web Proxy Server

ELEC 331 201
TO RUN: $ python proxy.py [server_ip e.g. localhost]
"""

from socket import *
import sys

if len(sys.argv) <= 1:
	print('Usage : "python proxy.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
	
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(('',6969))
tcpSerSock.listen(1)

while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)

	message = tcpCliSock.recv(1024).decode()
	print(message)
	# Extract the filename from the given message
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print('filename: '+filename)
	fileExist = "false"
	filetouse = "/" + filename
	print('filetouse: '+filetouse)

	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")                      
		outputdata = f.readlines()                        
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())            
		tcpCliSock.send("Content-Type:text/html\r\n".encode())

		# reading the cached file byte by byte
		for i in range(0, len(outputdata)):
			tcpCliSock.send(outputdata[i].encode())
		print('Read from cache')   

	# Error handling for file not found in cache
	except IOError:
		print("FileExists: "+fileExist)
		if fileExist == "false": 
			# Create a socket on the proxyserver
			c = socket(AF_INET,SOCK_STREAM)
			hostn = filename.replace("http://","",1)         
			print('hostn: '+hostn)                                  
			try:
				# Connect to the socket to port 80
				c.connect((hostn,80))
				recv = c.recv(1024).decode()
				print(recv)
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				fileobj = c.makefile('r', 0)               
				fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")  
				# Read the response into buffer
				tmpBuf = fileobj.readlines()
				# Create a new file in the cache for the requested file. 
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				tmpFile = open("./" + filename,"wb")  
				for i in range(0, len(tmpBuf)):
					tmpFile.write(tmpBuf[i])
					tcpCliSock.send(tmpBuf[i].encode())
			except:
				print("Illegal request")                                               
		else:
			# HTTP response message for file not found
			tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
			tcpCliSock.send("Content-Type:text/html\r\n".encode())
	# Close the client and the server sockets    
	tcpCliSock.close() 


