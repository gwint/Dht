from subprocess import call, Popen

import socket
import sys
from time import strftime, gmtime
import os.path
import time
import hashlib
import base64
<<<<<<< HEAD
import json
from time import sleep
import struct
=======
import asyncio
import websockets
>>>>>>> allow_joins

SERVER_NAME = "Greg's Server"

host = ''
port = 9999

<<<<<<< HEAD
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
=======
async def control(websocket, path):
  now = "test"
  await websocket.send(now)

  ## Get port numbers from client
  port_list_str = await websocket.recv()

  port_list = list(map(int, port_list_str.strip('[]').split(',')))
  print(port_list)

  for port in port_list:
    Popen(["python", "server.py"] + [str(port)])
>>>>>>> allow_joins


<<<<<<< HEAD
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
=======
def main():
  start_server = websockets.serve(control, 'localhost', 9999)
>>>>>>> allow_joins

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()

main()
