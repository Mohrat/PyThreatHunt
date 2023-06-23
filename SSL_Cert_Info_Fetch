import ssl
import socket
from OpenSSL import crypto
context = ssl.create_default_context()
dom = ['www.google.com','facebook.com']
for i in range(0,len(dom)): 
    with context.wrap_socket(socket.socket(), server_hostname=dom[i]) as sock:
        sock.connect((dom[i], 443))
        cert = sock.getpeercert()
        print("*"*50)
        print(dom[i])
        print("Issuer: ", issuer)
        print("Subject: ", subject)
        print("Valid From: ", cert['notBefore'])
        print("Valid Until: ", cert['notAfter'])
        print("*"*50)
