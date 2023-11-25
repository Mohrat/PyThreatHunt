import ssl
import socket
from OpenSSL import crypto

# Create an SSL context
context = ssl.create_default_context()

# Fetch certificate information for google.com
with context.wrap_socket(socket.socket(), server_hostname="google.com") as sock:
    sock.connect(("google.com", 443))
    cert = sock.getpeercert()

# Print certificate information for google.com
print("Google.com:")
print("Issuer: ", cert['issuer'])
print("Subject: ", cert['subject'])
print("Valid From: ", cert['notBefore'])
print("Valid Until: ", cert['notAfter'])