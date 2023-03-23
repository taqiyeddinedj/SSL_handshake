#!/usr/bin/env python

import socket
from cryptography.fernet import Fernet
import ssl


#Create a TCP/IP socket and bind it to a specific port 
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



#Wrap the socket with SSL
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain("/home/touk/ssl_python/new.pem","/home/touk/ssl_python/private.key")
ssl_soc=context.wrap_socket(soc,server_hostname="localhost")  

# Trust the server's self-signed certificate
context.load_verify_locations("/home/touk/ssl_python/new.pem")

#ssl_soc = ssl.wrap_socket(soc, cert_reqs=ssl.CERT_REQUIRED, ca_certs='/home/touk/ssl_python/cert.pem')

#Connect to the SSL server :
server_address=('localhost', 5555)
ssl_soc.connect(server_address)

#send encrypted data : 

######Generate an symemtric encryption
key = Fernet.generate_key()
ssl_soc.send(key)

######Create an instance of frenet using the key
f = Fernet(key)

#Encrypt it !!
encrypted_data=f.encrypt(b"Hello from the client ")
ssl_soc.sendall(encrypted_data)

#Receive the encrypted response:
encrypted_response = ssl_soc.recv(1024)
decrypted_response = f.decrypt(encrypted_response)
print(f"Received {decrypted_response.decode()} from the server")


#CLose the SSL connection 
ssl_soc.close()
