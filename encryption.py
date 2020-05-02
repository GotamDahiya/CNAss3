'''
This file encrypts the messages between the server and the client. A common number is chosen as the seed which shuffles the entire ASCII range by generating a random seed number. This common number is like the public key for the toy application. If the numbers entered are different then a erroneous message will be displayed.
'''

import random
import sys
import io


class Encryption:
    def __init__(self,
                 msg:    str,
                 r_seed: int):
        self.msg = msg
        self.r_seed = r_seed
        self.char_in_order = [chr(x) for x in range(0,127)]
        
    def encrypt(self):  # Encryptin the message to be sent
        result = ''
        # print("encrypting")
        random.seed(self.r_seed)
        shuffled_list = [chr(x) for x in range(0,127)]
        random.shuffle(shuffled_list)
        
        for i in range(0,len(self.msg)):
            result += shuffled_list[self.char_in_order.index(self.msg[i])]
            pass
        
        return result
    
    def decrypt(self):  # Decrypting the received message
        result=''
        # print("decrypting")
        random.seed(self.r_seed)
        shuffeld_list = [chr(x) for x in range(0,127)]
        random.shuffle(shuffeld_list)
        
        for i in range(0,len(self.msg)):
            result += self.char_in_order[shuffeld_list.index(self.msg[i])]
            pass
        
        return result