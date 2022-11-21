import json
import socket
from abc import abstractmethod

from thread_return import ThreadWithReturn

# the format in which encoding and decoding will occur
FORMAT = "utf-8"
BUFFER_SIZE = 2048

class Base():
    def __init__(self, serverhost='localhost', serverport=10000, listen_num=100):
        # host and listening port of network peers/central server
        self.serverhost, self.serverport = serverhost, int(serverport)
        
        # create server TCP socket (for listening)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        self.socket.bind((serverhost, int(serverport)))
        self.socket.listen(listen_num)
        
        # peerlist: dict with key is peer name and value is tuple (host,port) 
        # Child class CentralServer: connected peers of a network peer
        # Child class NetworkPeer: list of registered peers managed by central server
        self.peerlist = {}
        # used for mapping from MESSAGE TYPE to corresponding function
        self.handlers = {}

    def add_handler(self, msgtype, function): 
        self.handlers[msgtype] = function

    def function_mapper(self, message):
        type_ = message['msgtype']
        data_ = message['msgdata']
        self.handlers[type_](data_)

    def recv_input_stream(self, conn):
        # receive from client 
        buf = conn.recv(BUFFER_SIZE)
        # deserialize (json type -> python type)
        message = json.loads(buf.decode(FORMAT))
        # map into function
        self.function_mapper(message)

    def recv(self):
        while True:
            # wait until receive a connection request -> return socket for connection from client
            conn, addr = self.socket.accept()
            input_stream = ThreadWithReturn(target=self.recv_input_stream, args=(conn,))
            input_stream.start()
            val = input_stream.join()
            if val == -1:
                return

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def client_send(address, msgtype, msgdata):
        # msgtype for mapping into corresponding function
        # msgdata contains sent data
        msg_special = 'file_content'
        if msg_special in msgdata:
            if isinstance(msgdata[msg_special], bytes):
                msgdata[msg_special] = msgdata[msg_special].decode(FORMAT)
        message = {'msgtype': msgtype, 'msgdata': msgdata}
        # serialize into JSON file for transmitting over network
        message = json.dumps(message).encode(FORMAT)
        # create client TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # request connection
            s.connect(address)
        except ConnectionRefusedError:
            print('Connection Error: Your Peer Refused')
            raise
        else:
            s.sendall(message)
        finally:
            s.close()
