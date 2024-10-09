#!/usr/bin/env python3

import socket
import arguments
import argparse

# Run 'python3 VPN.py --help' to see what these lines do
parser = argparse.ArgumentParser('Send a message to a server at the given address and prints the response')
parser.add_argument('--VPN_IP', help='IP address at which to host the VPN', **arguments.ip_addr_arg)
parser.add_argument('--VPN_port', help='Port number at which to host the VPN', **arguments.vpn_port_arg)
args = parser.parse_args()

VPN_IP = args.VPN_IP  # Address to listen on
VPN_PORT = args.VPN_port  # Port to listen on (non-privileged ports are > 1023)


def parse_message(message):
    # Parse the application-layer header into the destination SERVER_IP, destination SERVER_PORT,
    # and message to forward to that destination
    #raise NotImplementedError("Your job is to fill this function in. Remove this line when you're done.")
    #return parse_message(message)
    #return SERVER_IP, SERVER_PORT, message
    try:
        header, actual_message = message.split("||", 1)
        server_ip, server_port = header.split(":")
        return server_ip, int(server_port), actual_message
    except ValueError:
        raise ValueError("Malformed message format")

print("VPN server starting - listening for connections at IP", VPN_IP, "and port", VPN_PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((VPN_IP, VPN_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connection established with {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received client message: '{data}'")
            try:
                server_ip, server_port, actual_message = parse_message(data)
                print(f"Parsed message to be forwarded to {server_ip}:{server_port}")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
                    forward_socket.connect((server_ip, server_port))
                    forward_socket.sendall(bytes(actual_message, 'utf-8'))
                    response = forward_socket.recv(1024)
                    conn.sendall(response)
            except Exception as e:
                error_message = f"Error processing message: {str(e)}"
                print(f"Exception type: {type(e).__name__}, Arguments: {e.args}")
                conn.sendall(bytes(error_message, 'utf-8'))
                print(error_message)


print("VPN server is done!")


### INSTRUCTIONS ###
# The VPN, like the server, must listen for connections from the client on IP address
# VPN_IP and port VPN_port. Then, once a connection is established and a message recieved,
# the VPN must parse the message to obtain the server IP address and port, and, without
# disconnecting from the client, establish a connection with the server the same way the
# client does, send the message from the client to the server, and wait for a reply.
# Upon receiving a reply from the server, it must forward the reply along its connection
# to the client. Then the VPN is free to close both connections and exit.

# The VPN server must additionally print appropriate trace messages and send back to the
# client appropriate error messages.