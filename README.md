# Multicast Heartbeat Receiver #

While working on deploying and validating multicast configurations I found the need for a simple 
utility that could join a multicast group and receive messages. I couldn't find anything basic
that fit, so I started looking into creating my own utility using Python.

I found a few standard code patterns that was what I was looking for at the core,
so I decided to repurpose them into this Multicast Heartbeat Receiver script/app.

### Summary: ###

* Version 1
* Used to receive multicast heartbeats from a group/channel specified via command line.

### Run: ###
multicast-receiver.py is designed to work with my multicast-sender.py script/app but it can be used
to receive multicast messages from any source:

* ./multicast-receiver.py [LOCAL BIND IP] [MULTICAST GROUP] [PORT]
* ./multicast-receiver.py 0.0.0.0 239.0.1.2 5004
* python3 multicast-receiver.py 0.0.0.0 239.0.1.2 5004
