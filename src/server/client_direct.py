



import sys
import time
from test_mgtd import test_defs
from src import defs
import logging
#cd_logger = logging.getLogger(__name__)

logging.basicConfig(filename='client.log', filemode='w', level=logging.DEBUG)
logging.info('Logging (client direct) Started')

cd_logger = logging.getLogger(__name__)

class client(object):
    def __init__(self, server):
        self.server = server
        self.f = open('clientlog.log','w')

    def operate(self): # testing. reads from test commands
        wait_for_user = 0
        cnt = 1
        tl = test_defs.test_commands
        for comm in list(reversed(defs.auto_first_commands_list)): #since in prod is run last command first, here also
            tl.insert(0,comm)
        #######################################################################
        # comment in and out following two lines to build db or run test_commands
        #########################################################################    
        for m in tl: # to run test commands
        #for m in test_defs.build_db: # to build DB for testing
            print(str(cnt).zfill(4) + ":" + m)
            cnt += 1
            if (defs.die_word in m[0:5]):
                print('client: got a die command', file=sys.stdout)
                break
            #check if command is 'import' and iterate over the file, calling each like teh else below
            if "turn on" in m[0:9]:
                wait_for_user = 1
            else:
                l = str(len(m)+5)
                sl = "{:0>4}:".format(l)
                slm = sl + m
                if wait_for_user != 0:
                    input('hit any key to send this message')
                message =  slm
                cd_logger.debug('client script sending {}'.format(message))
                recieved_data = self.server.command(message)
                self.f.write(str(cnt).zfill(4) + ":" + "\n" + message+"\n")
                self.f.write(recieved_data+"\n"+"\n")
                print("\nServer Said:")
                print(recieved_data+"\n")
                cd_logger.debug("ServerSaid: {}".format(recieved_data))

        print('client: closing socket', file=sys.stdout)
        cd_logger.debug("Client closing socket")
        self.f.close()
        #input("OK?")




