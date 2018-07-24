from subprocess import call, Popen

import socket
import sys
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
  port_list_str = await websocket.recv()

  port_list = list(map(int, port_list_str.strip('[]').split(',')))
  print(port_list)

  for port in port_list:
    Popen(["python", "server.py"] + [str(port)])


def main():
  start_server = websockets.serve(control, 'localhost', 9999)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()

main()
