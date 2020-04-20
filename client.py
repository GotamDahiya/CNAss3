import socket
import io
import random
import sys
import struct
from encryption import *
from udp_reliable import *


if __name__ == '__main__':
	severAddrPort = ("127.0.0.1",8989)
	bufferSize = 1024

	localIP = "127.0.0.2"
	localPort = 8080

	print("Client and server should have the same seed number(Public key)")
	r_seed=input("Enter number for seed function(Public key)-> ")

	clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	# clientSocket.bind((localIP,localPort))

	while True:
		
		msgFromClient = input("Enter a message-> ")
		msgFromClient = Encryption(msgFromClient,r_seed).encrypt()
		bytesToSend = msgFromClient.encode()
		
		clientSocket.sendto(bytesToSend, severAddrPort)
  
		msgFromServer = clientSocket.recvfrom(bufferSize)
		msgFromServer = msgFromServer[0].decode()
		msgFromServer = Encryption(msgFromServer,r_seed).decrypt()
		msg = "\nMessage from server:\n{}".format(msgFromServer)

		print(msg)