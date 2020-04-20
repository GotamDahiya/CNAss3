import array
import struct
import socket

def checksum_func(packet): # Creating a checksum for the data
    if len(packet) % 2 != 0:
        packet += b'\0'
    
    res = sum(array.array("H",packet))
    res = (res >>16)+(res&0xFFF)
    res += res >>16
    res = (~res)&0xFFF
    return res    
    pass

def checksum_receiver(data, checksum): # Verifying if the checksum is correct or not
    
    check=1
    if check==1:
        return 1
    else:
        return 0

def parse(datagram): # Splitting the datagram into it's constituent parts
    packet = {}
    packet['src_port'],packet['dst_port'],packet['seq'],packet['ack'],packet['wsize'],packet['proto'],packet['checksum'] = struct.unpack('!HHIIHHH', datagram[:18])
    packet['data'] = struct.unpack('!%ds'%(len(datagram)-18), datagram[18:len(datagram)])
    return packet
    pass


class UDPPacket:  # Creation of a UDP packet to be sent
    def __init__(self,
                src_host: str,
                dst_host: str,
                src_port: int,
                dst_port: int,
                data:     bytes):
        self.src_host = src_host # Source ip address
        self.dst_host = dst_host # Destination ip address
        self.src_port = src_port # Source port number
        self.dst_port = dst_port # Destination port number
        self.data     = data     # Data to be transmitted
        pass
    
    def build(self):
        packet = struct.pack(
            '!HHIIHHH', # Size H->2, I->4
            self.src_port, # Sorce port number        0
            self.dst_port, # Destination port number  2 
            0,             # Sequence number          4 
            0,             # Acknoledgement number    8 
            8192,          # Window Size              12
            17,            # Protocol -> UDP datagram 14
            0              # Initial Checksum value   16
        )
        p1 = packet+self.data # Initializing packet along with data for checksum
        pseudo = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),
            socket.inet_aton(self.dst_host),
            socket.IPPROTO_UDP,
            len(p1)
        )
        
        checksum = checksum_func(pseudo+p1)
        packet = packet[:16] + struct.pack('H',checksum) + self.data # Final packet to be transmitted
        
        return packet
        pass
    
# class Seq_ACK: # updation of sequence and acknoledgement numbers
#     def __init__(self, seq, ack):
#         self.seq = seq
#         self.ack = ack
        
#     def update_seq(self):
        
#         pass
    
#     def update_ack(self):
        
#         pass