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

NODES_FILE = "nodes.txt"
HOST = "localhost"
PORT = 9999

def create_nodes_file(port_list):
  nodes_file_obj = open(NODES_FILE, 'w')

  for port in port_list:
    nodes_file_obj.write("%s:%d\n" % (HOST, port))

  nodes_file_obj.close()

async def control(websocket, path):
  ## Get port numbers from client
  port_list_str = await websocket.recv()
  port_list = []

  if port_list_str[0] == '[':
    port_list = list(map(int, port_list_str.strip('[]').split(',')))
  else:
    print(port_list_str)

  for port in port_list:
    Popen(["python", "server.py"] + [str(port)])


def main():
  start_server = websockets.serve(control, 'localhost', PORT)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()

main()
