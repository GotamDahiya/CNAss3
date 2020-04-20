import random
import sys
import io

class Encryptio:
    def __init__(self,
                 msg:    str,
                 r_seed: int):
        self.msg = msg
        self.r_seed = r_seed
        self.char_in_order = [chr(x) for x in range(0,127)]
        
    def encrypt(self):
        result = ''
        random.seed(self.r_seed)
        shuffled_list = [chr(x) for x in range(0,127)]
        
        for i in range(0,len(msg)):
            result += shuffled_list[self.char_in_order.index(msg[i])]
            pass
        
        return result
    
    def decrypt(self):
        result=''
        random.seed(self.r_seed)
        shuffeld_list = [chr(x) for x in range(0,127)]
        
        for i in range(0,len(msg)):
            result += self.char_in_order[shuffeld_list.index(msg[i])]
            pass
        
        result += '\n'
        return result