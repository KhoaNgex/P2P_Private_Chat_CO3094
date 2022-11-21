import threading
from base import Base
from persistence import *

class CentralServer(Base):
    def __init__(self, serverhost='localhost', serverport=40000):
        super(CentralServer, self).__init__(serverhost, serverport)

        # get registered user list
        self.peerlist = get_all_users()

        # manage online user list
        self.onlinelist = {}
        
        # define handlers for received message of central server
        handlers = {
            'PEER_REGISTER': self.peer_register,
            'PEER_LOGIN': self.peer_login,
            'PEER_LIST': self.peer_list,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)
    
    ##==========implement protocol for user registration - central server==========##
    def peer_register(self, msgdata):
        # received register info (msgdata): peername, host, port, pass (hashed)
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        peer_password = msgdata['password']
        # register error if peer has been connected with central server
        # otherwise add peer to managed user list of central server
        if peer_name in self.peerlist:
            self.client_send((peer_host, peer_port), msgtype='REGISTER_ERROR', msgdata={})
            print (peer_name," has been refused for registration!")
        else:
            # add peer to managed user list
            self.peerlist.append(peer_name)
            # save to database
            add_new_user(peer_name,peer_password)
            self.client_send((peer_host, peer_port), msgtype='REGISTER_SUCCESS', msgdata={})
            print (peer_name," has been added to central server's managed user list!")
    ##===========================================================##

    ##==========implement protocol for authentication (log in) - central server==========##
    def peer_login(self, msgdata):
        # received login info (msgdata): peername, host, port, pass (hashed)
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        peer_password = msgdata['password']
        # login error if peer has not registered yet or password not match
        # otherwise add peer to online user list
        if peer_name in self.peerlist:
            # retrieve password
            peer_pass_retrieved = get_user_password(peer_name)
            if str(peer_password) == peer_pass_retrieved:
                # add peer to online user list
                self.onlinelist[peer_name] = tuple((peer_host, peer_port))
                self.client_send((peer_host, peer_port), msgtype='LOGIN_SUCCESS', msgdata={})
                print (peer_name," has been added to central server's online user list!")
            else:
                self.client_send((peer_host, peer_port), msgtype='LOGIN_ERROR', msgdata={})
                print (peer_name," has been refused for login!")
        else:
            self.client_send((peer_host, peer_port), msgtype='LOGIN_ERROR', msgdata={})
            print (peer_name," has been refused for login!")
    ##===========================================================##

    ##==========implement protocol for getting online user list - central server==========##
    def peer_list(self, msgdata): 
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        data = {'online_user_list': self.onlinelist}
        self.client_send((peer_host, peer_port), msgtype='LIST_ONLINE_USER', msgdata=data)
        print (peer_name," has been sent latest online user list!")
    ##===========================================================##

    def run(self):
        # A child thread for receiving message
        t = threading.Thread(target=self.recv)
        t.start()

if __name__ == '__main__':
    server = CentralServer()
    server.run()


