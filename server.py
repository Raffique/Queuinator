import socket
import select
import sys
'''Replace "thread" with "_thread" for python 3'''
from threading import Thread
from database import *
from design_patterns import singleton, Publisher
import time

@singleton
class Server(Publisher):

    def __init__(self, ip='localhost', port=8080):
        Publisher.__init__(self)

        self.ip = ip
    
        self.port = port
    
        self.list_of_clients = []

        self.runserver = True
        self.clientserver = True


    
    def clientthread(self, conn, addr):
    
        # sends a message to the client whose user object is conn
        conn.send(b"Welcome to this chatroom!")

        runner = True
    
        while runner and self.clientserver:
                try:
                    message = conn.recv(2048)
                    message = message.decode()
                    if message:
                        
                        """prints the message and address of the
                        user who just sent the message on the server
                        terminal"""
                        #print("<" + addr[0] + "> " + message)
    
                        # Calls broadcast function to send message to all
                        message_to_send = "<" + addr[0] + "> " + message
                        #self.broadcast(message_to_send, conn)
                        #self.broadcast(message, conn)
                        self.dispatch(message, conn)
    
                    else:
                        """message may have no content if the connection
                        is broken, in this case we remove the connection"""
                        self.remove(conn)
                        print("removed client")
                        runner = False
    
                except Exception as e:
                    print(e)
                    continue
        print("client loop exited...")
    
    """Using the below function, we broadcast the message to all
    clients who's object is not the same as the one sending
    the message """
    def broadcast(self, message, connection):
        for clients in self.list_of_clients:
            if clients!=connection or clients==connection:
                try:
                    clients.send(message.encode())
                    
                except:
                    clients.close()

                    # if the link is broken, we remove the client
                    self.remove(clients)
    
    """The following function simply removes the object
    from the list that was created at the beginning of
    the program"""
    def remove(self, connection):
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    def main(self):

        self.runserver = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(100)

        def run():

            while self.runserver:
            
                """Accepts a connection request and stores two parameters,
                conn which is a socket object for that user, and addr
                which contains the IP address of the client that just
                connected"""
                conn, addr = self.server.accept()
            
                """Maintains a list of clients for ease of broadcasting
                a message to all available people in the chatroom"""
                self.list_of_clients.append(conn)
            
                # prints the address of the user that just connected
                print (addr[0] + " connected")
            
                # creates and individual thread for every user
                # that connects
                Thread(target=self.clientthread, args=(conn,addr)).start()

            time.sleep(2)
            self.server.close()
            self.server.detach()
            print("close server....")
    

        #self.server.bind((self.ip, self.port))
        #self.server.listen(100)
        Thread(target=run).start()

    
    def stop(self):
        self.runserver = False
        self.closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.closer.connect((self.ip, self.port))
        self.closer.send("X_X".encode())
        time.sleep(1)
        self.closer.close()
        self.closer.detach()


if __name__ == "__main__":

    server = Server()
    server.main()