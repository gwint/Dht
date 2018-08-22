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
import json
import glob
import argparse
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/usr/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import RFile, RFileMetadata, NodeID, SystemException

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

NODES_FILE = "nodes.txt"
HOST = "localhost"
PORT = 9999


def create_nodes_file(port_list):
  nodes_file_obj = open(NODES_FILE, 'w')

  for port in port_list:
    nodes_file_obj.write("%s:%d\n" % (HOST, port))

  nodes_file_obj.close()

def generate_node_file(host_port_pairs):
  node_file_obj = open(NODES_FILE, 'w')
  for host, port in host_port_pairs:
    node_file_obj.write("%s:%d\n" % (host, port))
  node_file_obj.close()

def start_nodes(port_list):
  for port in port_list:
    Popen(["python", "server.py"] + [str(port)])

  ## Generate nodes.txt given list of ports and hosts
  generate_node_file([("127.0.0.1", port) for port in port_list])
  ## Then run init.py to populate finger tables
  Popen(["python", "init.py", NODES_FILE])

async def control(websocket, path, cmd_line_ports=[]):
  ## Get port numbers from client
  item_str = await websocket.recv()
  port_list = []

  if item_str[0] == '[':
    port_list = list(map(int, item_str.strip('[]').split(',')))
    start_nodes(port_list)
  else:
    command_obj = json.loads(item_str)
    print(command_obj)
    command_id = command_obj["command_id"]
    target = command_obj["target"]
    labels = command_obj["labels"]
    values = command_obj["values"]

    command_args = dict(zip(labels, values))

    if(command_id == "read_btn"):
      # Make socket
      transport = TSocket.TSocket(target["host"], target["port"])
      # Buffering is critical. Raw sockets are very slow
      transport = TTransport.TBufferedTransport(transport)
      # Wrap in a protocol
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      # Create a client to use the protocol encoder
      client = FileStore.Client(protocol)
      # Connect!
      transport.open()

      client.readFile(command_args["File Name:"], command_args["Owner:"])

def main():
  parser = argparse.ArgumentParser(description='Launch DHT nodes.')
  parser.add_argument("ports", metavar="Port", type=int, nargs='*',\
                      help="Ports on which to launch dht nodes")
  parser.add_argument('-wc', action="store_true",\
                      help="Use web client to submit ports")
  args = parser.parse_args()

  print(args.wc)

  if(args.wc):
    start_server = websockets.serve(control, 'localhost', PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
  else:
    start_nodes(args.ports)

main()
