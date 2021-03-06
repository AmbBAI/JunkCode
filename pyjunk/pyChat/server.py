'''
Created on 2012-2-15

@author: Amb
'''

import socket
import select
class ChatServer:
    def __init__(self, port):
        self.port = port
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind(("", port))
        self.srvsock.listen(5)
        self.descriptors = [self.srvsock]
        print 'ChatServer started on port %s' % port
 
    def run(self):
        while True:
            (sread, swrite, sexc) = select.select(self.descriptors, [], [])
            for sock in sread:
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    str = sock.recv(1024)
                    if str == ':q':
                        host, port = sock.getpeername()
                        str = 'Client left %s: %s\r\n' % (host, port)
                        self.broadcast_string(str, sock)
                        sock.send(':q')
                        sock.close()
                        self.descriptors.remove(sock)
                    else:
                        host, port = sock.getpeername()
                        newstr = '[%s:%s] %s' % (host, port, str)
                        self.broadcast_string(newstr, sock)
    

    def broadcast_string(self, str, omit_sock):
        for sock in self.descriptors:
            if sock != self.srvsock and sock != omit_sock:
                sock.send(str)
        print str

    
    def accept_new_connection(self):
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)
        newsock.send("You're connected to the Python chatserver")
        str = 'Client joined %s:%s' % (remhost, remport)
        self.broadcast_string(str, newsock)

myServer = ChatServer(2626)
myServer.run()

