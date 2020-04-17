import socket
import io

localIP = "127.0.0.1"
localPort = 8989
buffersize = 1024

serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

serverSocket.bind((localIP,localPort))

print("UDP server up and listening")

while True:
    bytesAddrPair = serverSocket.recvfrom(buffersize)
    message = bytesAddrPair[0]
    address = bytesAddrPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP:{}".format(address)

    print(clientMsg)
    print(clientIP)

    msgfromServer = input("Enter a message")
    bytesToSend = str.encode(msgfromServer)

    serverSocket.sendto(bytesToSend, address)
