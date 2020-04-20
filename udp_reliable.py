import array
import struct
import socket

def checksum_sender(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'
    
    res = sum(array.array("H",packet))
    res = (res >>16)+(res&0xFFF)
    res += res >>16
    res = (~res)&0xFFF
    return res    
    pass

def checksum_receiver(data, checksum):
    data_len = len(data)
    if(data_len %2) != 0:
        data += b'\0'
        
    res = sum(array.array("H",data))
    res = (res >>16)+(res&0xFFF)
    res += res >>16
    res = (~res)&0xFFF
    
    check = res+checksum
    return check

def parse(packet):
    packet = {}
    packet['src_port'],packet['dst_port'],packet['seq'],packet['ack'],packet['wsize'],packet['proto'],packet['checksum'] = struct.unpack('!HHIIHHH', packet)
    return packet
    pass
    

class UDPPacket:
    def __init__(self,
                src_host: str,
                dst_host: str,
                src_port: str,
                dst_port: str,
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
        p1 = packet+data # Initializing packet along with data for checksum
        pseudo = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),
            socket.inet_aton(self.dst_host),
            socket.IPPROTO_UDP,
            len(p1)
        )
        
        checksum = checksum_func(pseudo+packet)
        packet = packet[:16] + struct.pack('H',checksum) + self.data # Final packet to be transmitted
        
        return packet
        pass
    
class Seq_ACK:
    def __init__(self, seq, ack):
        self.seq = seq
        self.ack = ack
        
    def update_seq(self):
        
        pass
    
    def update_ack(self):
        
        pass