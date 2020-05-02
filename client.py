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
from buffer import *

if __name__ == '__main__':
	serverAddrPort = ("127.0.0.1",8989)
	bufferSize = 1024

	localIP = "127.0.0.2"
	localPort = 8080

	print("Client and server should have the same seed number(Public key)")
	r_seed=int(input("Enter number for seed function(Public key)-> "))

	# Creating server side UDP socket
	clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	clientSocket.bind((localIP,localPort)) # Binding this address to the socket whenever this program is run.
 
	seq, ack, = 0, 0

	while True:
		
		msgFromClient = input("Enter a message-> ")
		msgFromClient = Encryption(msgFromClient,r_seed).encrypt()
		data = msgFromClient.encode()
		bytesToSend = UDPPacket(localIP,serverAddrPort[0],localPort,serverAddrPort[1],seq,ack,data).build()
		add(seq, ack, bytesToSend)
		clientSocket.sendto(bytesToSend, serverAddrPort)
		

		datagram,ip_addr = clientSocket.recvfrom(bufferSize)
		packet = parse(datagram)
		# print(packet)
		datagram1 = datagram[:22] + datagram[24:]
		if(checksum_receiver(datagram1, packet['checksum']) and (packet['ack']-ack)<=1):
			
			msgFromServer, = packet['data']
			msgFromServer = msgFromServer.decode()
			msgFromServer = Encryption(msgFromServer,r_seed).decrypt()
			print("Message from server: ",end=' ')
			print(msgFromServer)
			print("Server's IP address:",end=' ')
			print(ip_addr,end='\n\n')
			ack = packet['ack'] + 1
			seq = packet['seq']
		else:
			
			print("Error! Either checksum is wrong or packet is not in sequence. Resend last message in full.")
			packet = render(seq, ack)
			msg, = Encryption(msg,r_seed).decrypt()
			print("Message from server: ",end=' ')
			print(msg)
			print("Server's IP address: ",end=' ')
			print(ip_addr,end='\n\n')
   
   
		msg, = packet['data']
		msg = msg.decode()
		msg = Encryption(msg,r_seed).decrypt()
		if(msg == "FIN"):
			sys.exit()