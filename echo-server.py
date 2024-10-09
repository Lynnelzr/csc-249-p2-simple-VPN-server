# !/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def process_operation(data):
    try:
        operation, arg1, arg2 = data.decode('utf-8').split(':')
        arg1, arg2 = float(arg1), float(arg2)
        if operation == 'converting to usd':
            return str(arg2 / arg1) if arg1 != 0 else 'Error: Division by zero'
        elif operation == 'converting from usd':
            return str(arg1*arg2)
        else:
            return 'Error: Unknown operation'
    except Exception as e:
        return f'Error: {str(e)}'

print("server starting - listening for connections at IP", HOST, "and port", PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected established with {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received client message: '{data.decode('utf-8')}' [{len(data)} bytes]")
            result = process_operation(data)
            print(f"sending result message '{result}' back to client")
            conn.sendall(result.encode('utf-8'))

print("server is done!")