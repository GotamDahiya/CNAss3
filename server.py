import socket
import io
import random
import sys
import struct
import encrpytion


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
        bytesFromClient = serverSocket.recvfrom(buffersize)
        msgFromClient = bytesFromClient[0].decode()
        address = bytesFromClient[1]
        msgFromClient = decrypt(msgFromClient,r_seed)
        clientIP = "Client IP:\n{}".format(address)
        clientMsg = "Message from Client:\n{}".format(msgFromClient)
        
        print(clientIP)
        print(clientMsg)

        msgFromServer = input("Enter a message-> ")
        msgFromServer = encrypt(msgFromServer,r_seed)
        bytesToSend = msgFromServer.encode()

        serverSocket.sendto(bytesToSend, address)
