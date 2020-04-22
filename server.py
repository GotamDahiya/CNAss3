import socket
import io
import random
import sys
import struct
from encryption import *
from udp_reliable import *

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
        
        datagram,ip_addr = serverSocket.recvfrom(buffersize)
        packet = parse(datagram)
        # print(packet)
        datagram1 = datagram[:22] + datagram[24:]
        if(checksum_receiver(datagram1, packet['checksum'])):
            
            msgFromClient, = packet['data']
            msgFromClient = msgFromClient.decode()
            msgFromClient = Encryption(msgFromClient, r_seed).decrypt()
            print("Clients ip address:")
            print(ip_addr)
            print("Message from client:")
            print(msgFromClient)
        else:
            print("Error! Packet Discarded")
            
            
        msgFromServer = input("Enter a message-> ")
        msgFromServer = Encryption(msgFromServer,r_seed).encrypt()
        data = msgFromServer.encode()
        bytesToSend = UDPPacket(localIP,ip_addr[0],localPort,ip_addr[1],data).build()
        serverSocket.sendto(bytesToSend,ip_addr)
