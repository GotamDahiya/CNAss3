'''
This file is used for creating the client side of the toy application. It sends a message to the server to establish a line of communication. The communication is done via terminal/command prompt.
IPv4 address -> 127.0.0.2
Port -> 8080
'''

import socket
import sys
import struct
from encryption import *
from udp_reliable import *


if __name__ == '__main__':
	serverAddrPort = ("127.0.0.1",8989)
	bufferSize = 1024

	localIP = "127.0.0.2"
	localPort = 8080

	print("Client and server should have the same seed number(Public key)")
	r_seed=input("Enter number for seed function(Public key)-> ")

	# Creating server side UDP socket
	clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	clientSocket.bind((localIP,localPort)) # Binding this address to the socket whenever this program is run.
 
	seq, ack, = 0, 0

	while True:
		
		msgFromClient = input("Enter a message-> ")
		msgFromClient = Encryption(msgFromClient,r_seed).encrypt()
		data = msgFromClient.encode()
		bytesToSend = UDPPacket(localIP,serverAddrPort[0],localPort,serverAddrPort[1],seq,ack,data).build()
		clientSocket.sendto(bytesToSend, serverAddrPort)
		

		datagram,ip_addr = clientSocket.recvfrom(bufferSize)
		packet = parse(datagram)
		# print(packet)
		datagram1 = datagram[:22] + datagram[24:]
		if(checksum_receiver(datagram1, packet['checksum'])):
			
			msgFromServer, = packet['data']
			msgFromServer = msgFromServer.decode()
			msgFromServer = Encryption(msgFromServer,r_seed).decrypt()
			print("Message from server:")
			print(msgFromServer)
			print("Server's IP address:")
			print(ip_addr)
			ack = packet['ack']+len(datagram[24:])+1
			seq = packet['seq']
			print(seq,end=' ')
			print(ack)
		else:
			print("Error! Resend last message in full.")