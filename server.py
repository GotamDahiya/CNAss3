''' 
This file is used for creating the server side of the toy application. It receives a message from the client and the user can send a message back to the client. Currently the communication is done via terminal/command prompt.
IPv4 Address -> 127.0.0.1
Port -> 8989
'''

import socket
import sys
import struct
from encryption import *
from udp_reliable import *
from buffer import *

if __name__ == '__main__':
    localIP = "127.0.0.1"
    localPort = 8989
    buffersize = 1024

    print("Server and client should have same seed number(Public Key)")
    r_seed = int(input("Enter number for seed function(Public key)-> "))

    # Creating server side UDP socket
    serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    serverSocket.bind((localIP,localPort))
    
    seq, ack = 0, 0
    
    print("UDP server up and listening")

    while True:
        
        datagram,ip_addr = serverSocket.recvfrom(buffersize)
        packet = parse(datagram)
        # print(packet)
        datagram1 = datagram[:22] + datagram[24:]
        if(checksum_receiver(datagram1, packet['checksum']) and (packet['seq']-seq)<=1):
            
            msgFromClient, = packet['data']
            msgFromClient = msgFromClient.decode()
            msgFromClient = Encryption(msgFromClient, r_seed).decrypt()
            print("Clients ip address:")
            print(ip_addr)
            print("Message from client:")
            print(msgFromClient,end='\n\n')
            seq = packet['seq'] + 1 
            ack = packet['ack']
        else:
            
            print("Error! Either checksum is wrong or packet is not in sequence. Obtaining message from container.")
            packet = render(seq, ack)
            msg, = packet['data']
            msg = Encryption(msg,r_seed).decrypt()
            print("Client's IP address: ",end=' ')
            print(ip_addr)
            print("Message from client: ",end=' ')
            print(msg,end='\n\n')
            
        msg, = packet['data']
        msg = msg.decode()
        msg = Encryption(msg,r_seed).decrypt()
        if(msg == "FIN"):
            data = "FIN"
            data = Encryption(data,r_seed).encrypt()
            data = data.encode()
            finalBytes = UDPPacket(localIP,ip_addr[0],localPort,ip_addr[1],seq,ack,data).build()
            serverSocket.sendto(finalBytes,ip_addr)
            sys.exit()
                    
        msgFromServer = input("Enter a message-> ")
        msgFromServer = Encryption(msgFromServer,r_seed).encrypt()
        data = msgFromServer.encode()
        bytesToSend = UDPPacket(localIP,ip_addr[0],localPort,ip_addr[1],seq,ack,data).build()
        add(seq, ack, bytesToSend)
        serverSocket.sendto(bytesToSend,ip_addr)