#!/usr/bin/python3

import socket
import sys
import struct
import signal


def handler(signum, frame):
    print('\nSIGNUM: ' + str(signum) + '\n' + 'FRAME: ' + str(frame) + '\n')
    res = input("Ctrl-c was pressed. Do you want to exit? y/n ")
    if res == 'y':
        exit(1)


signal.signal(signal.SIGINT, handler)


def help_and_exit(prog):
    print('Usage: ./multicast-receiver.py [BIND IP] [MCAST GROUP] [PORT]')
    print('Usage: ./multicast-receiver.py 0.0.0.0 239.0.1.2 5004')
    exit(1)


def mc_recv(fromnicip, mcgrpip, mcport):
    # This function is a modified pattern commonly found on the Internet.
    # Referenced and repurposed.

    # This creates a UDP socket
    # bufsize = 1024
    receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP, fileno=None)

    # This configures the socket to receive datagrams sent to this multicast
    # end point and must match the sender:
    # (multicast group ip address, mulcast port number)
    bindaddr = (mcgrpip, mcport)
    receiver.bind(bindaddr)

    # This joins the socket to the intended multicast group. The implications
    # are two. It specifies the intended multicast group identified by the
    # multicast IP address.  This also specifies from which network interface
    # (NIC) the socket receives the datagrams for the intended multicast group.
    # It is important to note that socket.INADDR_ANY means the default network
    # interface in the system (ifindex = 1 if loopback interface present). To
    # receive multicast datagrams from multiple NICs, we ought to create a
    # socket for each NIC. Also note that we identify a NIC by its assigned IP address.
    if fromnicip == '0.0.0.0':
        mreq = struct.pack("=4sl", socket.inet_aton(mcgrpip), socket.INADDR_ANY)
    else:
        mreq = struct.pack("=4s4s", socket.inet_aton(mcgrpip), socket.inet_aton(fromnicip))

    receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Receive and print the mssages
    while True:
        print('\nWaiting to Receive Multicast Heartbeat:')
        buf, senderaddr = receiver.recvfrom(1024)
        print('RECEIVED MULTICAST HEARTBEAT %s bytes from %s' % (len(buf), senderaddr))
        print("<-- " + mcgrpip + ":" + str(mcport) + ": " + str(buf.decode("utf-8")))


def main(argv):
    if len(argv) < 4:
        help_and_exit(argv[0])

    # Input validation can be added prior to assigning vars or passing prams:
    fromnicip = argv[1]
    mcgrpip = argv[2]
    mcport = int(argv[3])

    mc_recv(fromnicip, mcgrpip, mcport)


if __name__ == '__main__':
    main(sys.argv)
