import socket
from threading import Thread
from time import sleep
import struct

#this is the multicast function that is used to announce the central system's ip address and port number
def mdns():

    #there should probably be a  getter function to get current port number used by server
    message = b'8000'

    #there should be a setter function that sets the multicast group ip and port address
    #these values should be default 
    multicast_group = ('224.0.0.1', 7000)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    while True:
        sleep(1)
        sock.sendto(message, multicast_group)

#run the multicast function in a thread so it doesnt interefere with central system
Thread(name='mdns', target=mdns).start()