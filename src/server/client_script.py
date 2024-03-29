


import socket
import sys

#if 'C:\\Users\\oeitam\\PycharmProjects\\weekly' not in sys.path:
#    sys.path.append(r'C:\Users\oeitam\PycharmProjects\weekly')

if 'C:\\Users\\oeitam\\OneDrive - Intel Corporation\\Documents\\Z-Work\\Projects\\mgtd' not in sys.path:
    sys.path.append(r'C:\Users\oeitam\OneDrive - Intel Corporation\Documents\Z-Work\Projects\mgtd')



import os
import time
from src import defs
if  defs.mode != 'prod':
    from test_mgtd import test_defs

import logging
c_logger = logging.getLogger(__name__)

logging.basicConfig(filename='client.log', filemode='w', level=logging.DEBUG)
logging.info('Logging (into clienr.log) Started')

##############################

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address, file=sys.stdout)
sock.connect(server_address)
wait_for_user = 0
cnt = 1
try:
    if defs.mode != 'prod':
        lenm = len(test_defs.test_commands)
    else:
        lenm = 0
    mpos = 0

    while True:
    #for m in test_defs.test_commands:
        if defs.mode == 'socket':
            m = test_defs.test_commands[mpos]
            mpos += 1
        time.sleep(1)

        #else:
        if defs.mode == 'prod':
            if defs.auto_first_commands > 0 : # taking first auto commands
                m = defs.auto_first_commands_list[defs.auto_first_commands-1]
                defs.auto_first_commands -= 1
            else: # regular mode
                m = input("Client say:\n")
        # if m is just an empty line
        if not m.strip():
            #print("this is an empty line\n")
            continue
        # adding length
        l = str(len(m)+5)
        sl = "{:0>4}:".format(l)
        slm = sl + m
        if wait_for_user != 0:
            input('hit any key to send this message')
        print(str(cnt).zfill(8) + ":" + m)
        cnt += 1
        if (defs.die_word in m[0:5]) or (mpos-1) == lenm:
            print('client: got a die command', file=sys.stdout)
            sock.sendall(m.encode())
            time.sleep(1)
            break
        if "turn on" in m[0:9]:
            wait_for_user = 1
        message =  slm
        c_logger.debug('client script sending {}'.format(message))
        sock.sendall(message.encode())
        amount_received = 0
        amount_expected = 4096 # arbitrary
        got_first_part = 0
        save_counter = 0
        recieved_data = ''
        try:
            while amount_received < amount_expected:
                #print('amount rec: {}, amount exp {}'.format(amount_received, amount_expected))
                save_counter += 1
                if save_counter > 1000 :
                    print('save_counter over 1000. breaking!')
                    raise AssertionError
                data = sock.recv(1024)
                if len(data) == 0:
                    continue
                data=data.decode()
                if got_first_part == 0:
                    got_first_part = 1
                    l,d,data = data.partition(':')
                    amount_expected = int(l)
                    amount_received += len(data)+len(l)+len(d)
                else:
                    amount_received += len(data)
                recieved_data += data

        except AssertionError:
            c_logger.debug("Client recieve loop excceeded 1000 iterations on message {}".format(message))
            break

        time.sleep(1)
        print("\nServer Said:\n")
        print(recieved_data+"\n")
        c_logger.debug("Server Said: {}".format(recieved_data))


finally:
    print('client: closing socket', file=sys.stdout)
    c_logger.debug("Client closing socket")
    #input("OK?")
    sock.close()





