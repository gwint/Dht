from subprocess import call, Popen

import socket
import sys
from thread import *
from time import strftime, gmtime
import os.path
import time
import hashlib
import base64

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
      init_request = conn.recv(4096)
      print(init_request)

      request_pieces = init_request.split('\r\n')
      print(request_pieces[-4])

      request_key = request_pieces[-4].split(': ')[1]
      new_key = request_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
      hashed_new_key = hashlib.sha1(new_key).hexdigest()
      print(hashed_new_key)

      encoded_hashed_new_key = base64.b64encode(hashed_new_key)
      print(encoded_hashed_new_key)

      response = "HTTP/1.1 101 Switching Protocols\n" + \
                 "Upgrade: websocket\n" + \
                 "Connection: Upgrade\n" + \
                 "Sec-WebSocket-Accept: %s\n" % encoded_hashed_new_key

      conn.sendall(response)

      ## Form response and send back to client
      resp = conn.recv(4096)
      print(resp)

      ## Wait to recieve port list from client

      for port in range(19000, 19004):
        Popen(["python", "server.py"] + [str(port)])

      ## Create nodes.txt

      ## Initalize dht
  except KeyboardInterrupt:
    s.shutdown(socket.SHUT_RDWR)
    s.close()


main()
