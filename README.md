## Computer Networls Assignment 3
This assignment asks for an application layer to be built using UDP sockets with reliability built into them.

A simple chat application is made which is run on a local machine.

Two programs run: 
	* **A server.py which allows for a message to be recieved from the client and outputs a designated statement.*
	* **A client.py which sends a message to the server and receives a designated statement.*

The messages which are passed between server and client are encrpyted using random.seed() function which shuffles the aplhanumerals stored in each program.

The packet transmitted between the server and client contains a sequence, acknowledgement, checksum, source address, destination address and encrypted data.
