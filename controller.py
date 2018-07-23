from subprocess import call, Popen

import socket
import sys
#from thread import *
from time import strftime, gmtime
import os.path
import time
import hashlib
import base64
import asyncio
import websockets

SERVER_NAME = "Greg's Server"

host = ''
port = 9999

async def time(websocket, path):
    while True:
        now = "test"
        await websocket.send(now)
        await asyncio.sleep(3)

def main():
  start_server = websockets.serve(time, 'localhost', 9999)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()
  '''
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    global port
    s.bind((host, port))
  except socket.error as e:
    print(str(e))

  s.listen(5)

  print("Waiting for connections")

  try:
    ##while True:
      #conn, addr = s.accept()
      #print(addr)
      #init_request = conn.recv(4096)
      #print(init_request)

      #request_pieces = init_request.split('\r\n')
      #print(request_pieces[-4])

      #request_key = request_pieces[-4].split(':')[1].strip()
      #new_key = request_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
      #hashed_new_key = hashlib.sha1(new_key).digest()
      #print(hashed_new_key)

      #encoded_hashed_new_key = base64.b64encode(hashed_new_key)
      #print(encoded_hashed_new_key)

      #response = "HTTP/1.1 101 Switching Protocols\r\n" + \
      #           "Upgrade: websocket\r\n" + \
      #           "Connection: Upgrade\r\n" + \
      #           "Sec-WebSocket-Accept: %s\r\n" % encoded_hashed_new_key + \
      #           "WebSocket-Origin: http://localhost\r\n\n"

      #conn.sendall(response)

      ## Wait to recieve port list from client

      for port in range(19000, 19004):
        Popen(["python", "server.py"] + [str(port)])

      ## Create nodes.txt

      ## Initalize dht
  except KeyboardInterrupt:
    s.shutdown(socket.SHUT_RDWR)
    s.close()
  '''

main()
