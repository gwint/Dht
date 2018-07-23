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

async def control(websocket, path):
  now = "test"
  await websocket.send(now)

  ## Get port numbers from client
  port_list = await websocket.recv()
  print(port_list)
  print(type(port_list))
  print(list(port_list))

  for port in range(19000, 19004):
    Popen(["python", "server.py"] + [str(port)])


def main():
  start_server = websockets.serve(control, 'localhost', 9999)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()

main()
