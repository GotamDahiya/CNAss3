import socket
import io
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

    result+='\n'
	return result

if __name__ == '__main__':
    localIP = "127.0.0.1"
    localPort = 8989
    buffersize = 1024

    print("Server and client should have same seed number(Public Key)")
    r_seed = input("Enter number for seed function(Public key)-> ")

    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    serverSocket.bind((localIP,localPort))

    print("UDP server up and listening")

    while True:
        bytesAddrPair = serverSocket.recvfrom(buffersize)
        msgFromClient = bytesAddrPair[0]
        address = bytesAddrPair[1]
        msgFromClient = msgFromClient.decode()
        msgFromClient = decrypt(msgFromClient,r_seed)
        clientMsg = "Message from Client:{}".format(msgFromClient)
        clientIP = "Client IP:{}".format(address)

        print(clientMsg)
        print(clientIP)

        msgFromServer = input("Enter a message-> ")
        msgFromServer = encrypt(msgFromServer,r_seed)
        bytesToSend = msgFromServer.encode()

        serverSocket.sendto(bytesToSend, address)
