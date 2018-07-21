from subprocess import call, Popen

import socket
import sys
from thread import *
from time import strftime, gmtime
import os.path
import time
import hashlib
import base64
import json
from time import sleep
import struct

SERVER_NAME = "Greg's Server"

host = ''
port = 9999

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    global port
    s.bind((host, port))
  except socket.error as e:
    print(str(e))

  s.listen(5)

  print("Waiting for connections")

  try:
    while True:
      conn, addr = s.accept()
      #print(addr)
      init_request = conn.recv(4096)
      #print(init_request)

      request_pieces = init_request.split('\r\n')
      #print(request_pieces[-4])

      request_key = request_pieces[-4].split(':')[1].strip()
      new_key = request_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
      hashed_new_key = hashlib.sha1(new_key).digest()
      #print(hashed_new_key)

      encoded_hashed_new_key = base64.b64encode(hashed_new_key)
      #print(encoded_hashed_new_key)

      response = "HTTP/1.1 101 Switching Protocols\r\n" + \
                 "Upgrade: websocket\r\n" + \
                 "Connection: Upgrade\r\n" + \
                 "Sec-WebSocket-Accept: %s\r\n" % encoded_hashed_new_key + \
                 "WebSocket-Origin: http://localhost:9999\r\n\n"

      conn.sendall(response)

      conn.settimeout(None)
      sleep(5)
      ## Form response and send back to client
      resp = conn.recv(1024)
      print(struct.unpack("<L", resp)[0])
      #print(str(bytes(resp)))

      ## Wait to recieve port list from client

      for port in range(19000, 19004):
        Popen(["python", "server.py"] + [str(port)])

      ## Create nodes.txt

      ## Initalize dht
  except KeyboardInterrupt:
    s.shutdown(socket.SHUT_RDWR)
    s.close()


main()
