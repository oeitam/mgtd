
import socket
import sys
import os
import time
from datetime import datetime
import shutil
from subprocess import Popen, CREATE_NEW_CONSOLE
from src import defs
from src.server import client_direct

import logging
logger = logging.getLogger(__name__)



class Server(object):
    def __init__(self, gtd):
        print('server init')
        self.gtd = gtd
        if defs.mode == 'direct':
            self.client = client_direct.client(self)

    # start_the_client method starts the client seperate process
    def start_the_client(self):
        if defs.mode == 'direct' or defs.mode == 'prod':
            return
        print("Launching the client in mode: " + defs.mode)
        print(os.getcwd())
        pc = Popen([sys.executable, 'src/server/client_script.py'],
                   creationflags=CREATE_NEW_CONSOLE)

        time.sleep(1)
        if pc.returncode == 63:
            print("Client could not initilize properly", file=sys.stderr)
        print('class Server initialized', file=sys.stderr)

        # setup variables
        self.client_process = pc


    def command(self, ldata):
        a, b, data = ldata.partition(':')
        self.gtd.take_data(data)
        if self.gtd.process():  # gtd to process the latest data it recieved
            return_message = self.gtd.get_message_back_to_client()
        else:
            return_message = "Illegal command was not processed"
        # return_message = defs.mlt
        l = str(len(return_message) + 5)
        sl = "{:0>4}:\n".format(l)
        slm = sl + return_message
        logger.debug('return_message: %s', slm)
        #print("--" + slm + "--")
        return slm

    def zip_data(self):
        today_str = datetime.now().strftime("%Y%m%d-%H%M")
        output_filename = defs.mgtd_code_path + '\datastore\\' + today_str
        source_dir = defs.mgtd_local_path
        shutil.make_archive(output_filename, format='zip', root_dir=source_dir)
        # adding - also copying one of the html (so can view on teh phone for example)
        # TODO note - here we support only 'production' mode
        if defs.mode == 'prod':
            shutil.copy(defs.mgtd_local_path + '\production\\' + 'list_html_production_hier.html', defs.mgtd_code_path + '\datastore\\' + 'list_html_production_hier.html' )


    # server_process method is the main method of the server
    # crates a socket from the server for the client to use
    # once requests are coming from the client, it sends it to
    # the gtd for processing
    def server_process(self):
        if defs.mode == 'direct': # used for testing, I think
            self.client.operate()
            self.zip_data()
            return
        print('Starting the communications server')
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print('starting up on %s port %s' % server_address, file=sys.stderr)
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # start the slient
        self.start_the_client() # practically only in dev mode ????

        while True:
            # Wait for a connection
            print('waiting for a connection', file=sys.stderr)
            connection, client_address = self.sock.accept()
            try:
                print('connection from', client_address, file=sys.stderr)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    print('recieved "%s"' % data.decode(), file=sys.stderr)
                    if ":" in data.decode():
                        [t1, t2] = data.decode().split(":",1) # t2 gets the actual what sent by client w/o the number of chars
                    else:
                        t2 = data.decode()
                    if (defs.die_word in t2[:3]): # 'die' would be here in case of die
                    # if (defs.die_word in data.decode()):
                        print('server: Dieing!!!')
                        #raise
                        break
                    if data:
                        #check here if the data is 'import' -> execute the file over teh code below
                        print('sending data to the proc', file=sys.stderr)
                        # remove the length of data from the top of the string
                        a,b,data = data.decode().partition(':')
                        self.gtd.take_data(data)
                        try:
                            self.gtd.process() # gtd to process the latest data it recieved
                        except:
                            SyntaxError
                        # once the process method is done, it means data is ready for the
                        return_message = self.gtd.get_message_back_to_client()
                        # return_message = defs.mlt
                        l = str(len(return_message) + 5)
                        sl = "{:0>4}:".format(l)
                        slm = sl + return_message
                        logger.debug('return_message: %s', slm)
                        print("--"+slm+"--")
                        connection.sendall(slm.encode())
                    else:
                        print('no more data from ', client_address, file=sys.stderr)
                        break

            finally:
                # Clean up the connection
                print('Zipping and saving datebase\n')
                self.zip_data()
                print('server: Closing socket', file=sys.stdout)
                connection.close()
                break
        print('server off')






