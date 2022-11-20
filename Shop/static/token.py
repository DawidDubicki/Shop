import binascii
import os
token = os.urandom(20)
print(len(binascii.hexlify(token).decode()))