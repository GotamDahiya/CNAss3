import socket
import random
import sys

def encrypt(msg,r_seed):
	result = ''
	char_in_order = [chr(x) for x in range(0,127)]

	random.seed(r_seed)
	shuffled_list = [chr(x) for x in range(0,127)]
	random.shuffle(shuffled_list)

	for i in range(0, len(msg)):
		result += shuffled_list[char_in_order.index(msg[i])]

	return result

def decrypt(msg,r_seed):
	result=''
	char_in_order = [chr(x) for x in range(0,127)]

	random.seed(r_seed)
	shuffled_list = [chr(x) for x in range(0,127)]
	random.shuffle(shuffled_list)

	for i in range(0, len(msg)):
		result += char_in_order[shuffled_list.index(msg[i])]

	result += '\n'
	return result

if __name__ == '__main__':
	severAddrPort = ("127.0.0.1",8989)
	bufferSize = 1024

	localIP = "127.0.0.2"
	localPort = 8080

	r_seed=input("Enter number for seed function-> ")

	clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	# clientSocket.bind((localIP,localPort))

	while True:
		
		msgFromClient = input("Enter a message-> ")
		msgFromClient = encrypt(msgFromClient,r_seed)
		bytesToSend = msgFromClient.encode()
		
		clientSocket.sendto(bytesToSend, severAddrPort)

		msgFromServer = clientSocket.recvfrom(bufferSize)
		msgFromServer = msgFromServer[0].decode()
		msgFromServer = decrypt(msgFromServer,r_seed)
		msg = "Message from server {}".format(msgFromServer)

		print(msg)