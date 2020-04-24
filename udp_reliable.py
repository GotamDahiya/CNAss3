'''
This file creates the raw packets to be transmitted via the UDP connection. It includes a checksum generator and verifier, packet builder.
'''

import array
import struct
import socket


def checksum_func(packet): # Creating a checksum for the data
    checksum = 0
    data_len = len(packet)
    if(data_len % 2) != 0:
        data_len += 1
        packet += b'\0'
        
    for i in range(0,data_len,2):
        w = (packet[i] << 8) + (packet[i+1])
        checksum += w
    
    checksum = (checksum>>16) + (checksum&0xFFFF)
    checksum = (~checksum)&0xFFFF
    return checksum
    pass

def checksum_receiver(data, checksum): # Verifying if the checksum is correct or not
    data_len = len(data)
    if data_len%2 != 0:
        data_len += 1
        data += b'\0'
        
    for i in range(0,data_len,2):
        w = (data[i] << 8) + data[i+1]
        checksum += w
    
    checksum = (checksum>>16) + (checksum&0xFFFF)
    if checksum==0xFFFF:
        return 1
    else:
        return 0

def parse(datagram): # Splitting the datagram into it's constituent parts
    packet = {}
    packet['src_port'],packet['dst_port'],packet['src_host'],packet['dst_host'],packet['seq'],packet['ack'],packet['wsize'],packet['checksum'] = struct.unpack('!HH4s4sIIHH', datagram[:24])
    packet['data'] = struct.unpack('!%ds'%(len(datagram)-24), datagram[24:])
    return packet
    pass


class UDPPacket:  # Creation of a UDP packet to be sent
    def __init__(self,
                src_host: str,
                dst_host: str,
                src_port: int,
                dst_port: int,
                seq:      int,
                ack:      int,
                data:     bytes):
        self.src_host = src_host # Source ip address
        self.dst_host = dst_host # Destination ip address
        self.src_port = src_port # Source port number
        self.dst_port = dst_port # Destination port number
        self.data     = data     # Data to be transmitted
        self.seq      = seq      # Sequence number of packet being transmitted
        self.ack      = ack      # Acknoledgement number of packet being transmitted
        pass
    
    def build(self):
        packet = struct.pack(
            '!HH4s4sIIHH', # Size H->2, I->4, 4s->4
            self.src_port,                    # Sorce port number         0
            self.dst_port,                    # Destination port number   2
            socket.inet_aton(self.src_host),  # Source IPv4 address       4
            socket.inet_aton(self.dst_host),  #  Destination IPv4 address 8
            self.seq,                         # Sequence number           12 
            self.ack,                         # Acknoledgement number     16 
            8192,                             # Window Size               20
            0                                 # Initial Checksum value    22
        )
        p1 = packet+self.data # Initializing packet along with data for checksum
        # print(p1)
        # print(self.data)
        
        checksum = checksum_func(p1)
        # print(checksum)
        packet = packet[:22] + struct.pack('!H',checksum) + self.data # Final packet to be transmitted
        
        return packet
        pass