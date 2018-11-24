#!/usr/bin/env python
import sys
import socket
import time
import base64
import cryptanalib

def get_response(sock):
    resp = ""

    while "ciphertext" not in resp:
      resp += sock.recv(4096)
      time.sleep(0.01)
      
    return resp

def request(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], int(sys.argv[2])))

    resp = get_response(sock)
    data = base64.b64encode(data)    
    sock.send(data + "\r\n")
    resp = get_response(sock)
    sock.close()

    return ("OK!" in resp)

def crack():
    data = base64.b64decode(
      "irRmWB7oJSMbtBC4QuoB13DC08NI06MbcWEOc94q0OXP" \
      "bfgRm+l9xHkPQ7r7NdFjo6hSo6togqLYITGGpPsXdg=="
    )

    cryptanalib.padding_oracle_decrypt(request, data, 16, verbose=True)
    
def usage():
    print "Usage: %s <host> <port>" % sys.argv[0]
    sys.exit()
    
def main():
    if len(sys.argv) < 3:
        usage()
        
    crack()
  
if __name__ == "__main__":
    main()
