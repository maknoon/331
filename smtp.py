"""
Programming Assignment #3: Simple SMTP Client

ELEC 331 201
TO RUN: $ python smtp.py
NOTES: Execute this script on the ECE server.
	   Screenshots for expected behavior (and proof of sent email) are
	   attached in screenshots/.
"""

from socket import *

msg = "\r\n I love computer networks!"
msg1 = "\r\n But sometimes they frustrate me :("
endmsg = "\r\n.\r\n"
error220 = '220 reply not received from server.'
error250 = '250 reply not received from server.'
error354 = '354 reply not received from server.'
error221 = '221 reply not received from server.'

# Choose a mail server (e.g. Google mail server) and call it mailserver
# Edit: told to use the ece mail server
mailserver = 'mx1.ece.ubc.ca'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET,SOCK_STREAM)
print('Connecting to mailserver '+mailserver)
clientSocket.connect((mailserver,25)) # host is mailserver, smtp port is 25

recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '220':
	print(error220)

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
print('C: '+heloCommand)
recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '250':
    print(error250)
    
# Send MAIL FROM command and print server response.
mailfromCommand = 'MAIL FROM: <p6z8@ece.ubc.ca>\r\n'
clientSocket.send(mailfromCommand.encode())
print('C: '+mailfromCommand)
recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '250':
	print(error250)

# Send RCPT TO command and print server response. 
rcpttoCommand = 'RCPT TO: <conniemob@alumni.ubc.ca>\r\n'
clientSocket.send(rcpttoCommand.encode())
print('C: '+rcpttoCommand)
recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '250':
	print(error250)

# Send DATA command and print server response. 
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand.encode())
print('C: '+dataCommand)
recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '354':
	print(error354)

# Send message data.
# Message ends with a single period.
clientSocket.send(msg.encode())
print('C: '+msg)
clientSocket.send(msg1.encode())
print('C: '+msg1)
clientSocket.send(endmsg.encode())
print('C: '+endmsg)
recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '250':
	print(error250)

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand.encode())
print('C: '+quitCommand)
recv = clientSocket.recv(1024).decode()
print('S: '+recv)
if recv[:3] != '221':
	print(error221)

