'''
This file stores 20 packets for rendering in case of packet loss at either server side or client side.
The sequence and acknowledgement numbers act as index for storing the packets. This allows rendering of lost packet easier.
'''

import struct
import array
import io
from udp_reliable import *

container = {}

def add(seq: int, ack: int, packet: bytes):
    global container
    sum = seq+ack
    if(len(container) == 20):
        del container[abs(20-sum)]
    container[seq+ack] = packet
    pass

def render(seq: int, ack: int):
    packet = container[seq+ack]
    packet = parse(packet)
    return packet
    pass