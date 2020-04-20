import socket
import io
import random
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

	clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	clientSocket.bind((localIP,localPort))

	while True:
		msgFromClient = input("Enter a message-> ")
		msgFromClient = Encryption(msgFromClient,r_seed).encrypt()
		data = msgFromClient.encode()
		bytesToSend = UDPPacket(localIP,serverAddrPort[0],localPort,serverAddrPort[1],data).build()
		clientSocket.sendto(bytesToSend, serverAddrPort)

	
		datagram,ip_addr = clientSocket.recvfrom(bufferSize)
		packet = parse(datagram)
		# print(packet)
		if(checksum_receiver(datagram, packet['checksum'])):
			msgFromServer, = packet['data']
			msgFromServer = msgFromServer.decode()
			msgFromServer = Encryption(msgFromServer,r_seed).decrypt()
			print("Message from server:")
			print(msgFromServer)
			print("Server's IP address:")
			print(ip_addr)
		else:
			print("Error! Package discarded")