import random
import sys

result = ''
choice = ''
message = ''

char_in_order = [chr(x) for x in range(32,127)]

while choice != 0:
    choice = input("\n Do you want to encrypt or decrypt a message?\n1 to encrypt,2 to decrypt and 0 to exit. ")
    if str(choice) == '1':
        message = input("Enter message-> ")
        # print(type(message))
        r_seed = input("Enter seed for random number-> ")
        random.seed(r_seed)
        shuffled_list = [chr(x) for x in range(32,127)]
        random.shuffle(shuffled_list)

        for i in range(0, len(message)):
            result += shuffled_list[char_in_order.index(message[i])]
        
        print(result+'\n\n')
        result = ''

    elif str(choice)=='2':
        message = input("Enter message-> ")
        r_seed = input("Enter seed number-> ")
        random.seed(r_seed)

        shuffled_list=[chr(x) for x in range(32,127)]
        random.shuffle(shuffled_list)
        
        for i in range(0, len(message)):
            result += char_in_order[shuffled_list.index(message[i])]

        print(result+'\n\n')
        result = ''

    elif str(choice)=='0':
        sys.exit()