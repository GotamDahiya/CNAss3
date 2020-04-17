import socket

severAddrPort = ("127.0.0.1",8989)
bufferSize = 1024

localIP = "127.0.0.2"
localPort = 8080

clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.bind((localIP,localPort))

while True:
	
	msgFromClient = input("Enter a message")
	bytesToSend = str.encode(msgFromClient)
	
	clientSocket.sendto(bytesToSend, severAddrPort)

	msgfromServer = clientSocket.recvfrom(bufferSize)

	msg = "Message from server {}".format(msgfromServer[0])

	print(msg)