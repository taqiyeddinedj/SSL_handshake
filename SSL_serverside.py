#!/usr/bin/env python

import socket
import ssl
import threading
from cryptography.fernet import Fernet

#dont ask me why we need it 
HOST='localhost'
PORT=5555

#key = Fernet.generate_key()

#we create the TCP/IP Socket
soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Wrap the socket with SSL/TLS
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("/home/touk/ssl_python/new.pem", "/home/touk/ssl_python/private.key")
ssl_soc= context.wrap_socket(soc, server_side=True) 

# Trust the server's self-signed certificate
context.load_verify_locations("/home/touk/ssl_python/new.pem")

#let's bind the SSL_socket  
ssl_soc.bind((HOST,PORT))

#listen for incoming requests...
ssl_soc.listen()

#Accepting the incoming connections and handling it
def handle_connection(connection, client_address):
    print(f"Connection from {client_address}")
    key = connection.recv(1024)
    f = Fernet(key)

    #receive and encrypt the data from the client 
    #encrypted_data =  connection.recv(1024)
    message = "Hello, client!".encode()
    
    encrypted_data = f.encrypt(message)

    #decrypt the data and decode it :
    decrypted_data=f.decrypt(encrypted_data)
    print(f"Received {decrypted_data.decode()} from client {client_address}")

    #send an encrypted response :
    encrypted_response=f.encrypt(b"Hello from the SERVER!")
    connection.sendall(encrypted_response)

    connection.close()

while True:
    connection, client_address= ssl_soc.accept()
    thread = threading.Thread(target=handle_connection, args=(connection,client_address))
    thread.start()
