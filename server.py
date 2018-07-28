# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import glob
import sys
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/usr/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import NodeID, RFile, RFileMetadata, SystemException

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from socket import gethostbyname, gethostname

import init
import hashlib
import socket
from subprocess import Popen
from time import sleep

import logging
logging.basicConfig(level=logging.DEBUG)

NODE_ID = 0
SUCC_ID = 1
ITEM_ID = 2

class ChordHandler:
    def __init__(self):
        self.fingerTable = []
        self.contentHashes = []
        self.myNode = NodeID()
        port = int(sys.argv[1])
        ipAddr = gethostbyname(gethostname())
        idStr = gethostbyname(gethostname()) + ":" + sys.argv[1]
        key = hashlib.sha256(idStr).hexdigest()
        print(key)
        self.myNode.ip = ipAddr
        self.myNode.port = port
        self.myNode.id = key
        self.fileData = []

    def addFile(self, file_obj):
      ## check to see if node owns file, if not throw error
      self.fileData.append(file_obj)

    def removeFile(self, content_hash):
      for i in range(len(self.fileData)):
        if(file_obj.meta.contentHash == content_hash):
          self.fileData.pop(i)

    def getFiles(self):
      return self.fileData

    def addNode(self, host, port):
      new_node_key = hashlib.sha256(host + ":" + str(port)).hexdigest()
      new_node = NodeID()
      new_node.ip = host
      new_node.port = port
      new_node.id = new_node_key
      ## Make its fingertable (current node to find all answers)
      new_fingertable = []

      for i in range(256):
        finger_key = \
         hex((int(new_node_key, 16) + (2**i)) % (2**256)).strip("0x").strip('L')
        succ = self.findSucc(finger_key)

        if(self.contains(new_node_key, finger_key, succ.id)):
          new_fingertable.append(new_node)
        else:
          new_fingertable.append(self.findSucc(finger_key))

      ## Launch new server
      Popen(["python2", "server.py"] + [str(port)])
      sleep(3)

      ## Update other nodes fingertables
      transport = TSocket.TSocket(host, port)
      # Buffering is critical. Raw sockets are very slow
      transport = TTransport.TBufferedTransport(transport)
      # Wrap in a protocol
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      # Create a client to use the protocol encoder
      client = FileStore.Client(protocol)
      transport.open()

      client.setFingertable(new_fingertable)
      transport.close()

      new_node_succ = self.findSucc(new_node_key)
      new_node_pred = self.findPred(new_node_key)

      succ_files = []

      if(new_node_succ.id == new_node_key):
        succ_files = self.getFiles()
      else:
        ## Update other nodes fingertables
        transport = TSocket.TSocket(new_node_succ.ip, new_node_succ.port)
        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # Create a client to use the protocol encoder
        client = FileStore.Client(protocol)
        transport.open()

        succ_files = client.getFiles()
        transport.close()

      ## New node must take ownership of some files from successor,
      ## while successor must relinquish ownership of some
      for file_obj in succ_files:
        if(self.contains(file_obj.meta.contentHash,\
                         new_node_pred.id,\
                         new_node_key)):
          ## File belongs to new node
          if(new_node_succ.id == self.myNode.id):
            self.removeFile(file_obj.meta.contentHash)
          else:
            ## Update other nodes fingertables
            transport = TSocket.TSocket(new_node_succ.ip, new_node_succ.port)
            # Buffering is critical. Raw sockets are very slow
            transport = TTransport.TBufferedTransport(transport)
            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            # Create a client to use the protocol encoder
            client = FileStore.Client(protocol)
            transport.open()

            client.removeFile(file_obj.meta.contentHash)

          ## Update other nodes fingertables
          transport = TSocket.TSocket(host, port)
          # Buffering is critical. Raw sockets are very slow
          transport = TTransport.TBufferedTransport(transport)
          # Wrap in a protocol
          protocol = TBinaryProtocol.TBinaryProtocol(transport)
          # Create a client to use the protocol encoder
          client = FileStore.Client(protocol)
          transport.open()

          client.addFile(file_obj)

      ## Fingertables of other nodes need to be updated



    def writeFile(self, file_obj):
      file_name = file_obj.meta.filename

      succ = self.findSucc(file_obj.meta.contentHash)
      if(succ.id != self.myNode.id):
        raise SystemException("Cannot Write: Server does not own this file!")

      if file_obj.meta.contentHash in self.contentHashes:
        i = 0
        for obj in self.fileData:
          if obj.meta.contentHash != file_obj.meta.contentHash:
            i += 1
          else:
            break
        ##overwrite contents
        self.fileData[i].content = file_obj.content
        ##increment version number
        self.fileData[i].meta.version += 1
      else: ## file does not exist
        file_obj.meta.version = 0
        self.fileData.append(file_obj)
        version_num = 0
        self.contentHashes.append(file_obj.meta.contentHash)

    def readFile(self, filename, file_owner):
      hash = hashlib.sha256(filename +\
                            ":" + file_owner).hexdigest()
      succ = self.findSucc(hash)
      if(succ.id != self.myNode.id):
        raise SystemException("Cannot Read: Server does not own this file!")

      for obj in self.fileData:
        if obj.meta.contentHash == hash:
          return obj
      raise SystemException("Hash not found: Check owner or file name!")

    def showFingertable(self, a_list):
      for entry in a_list:
        print "port: ", entry.port

    def setFingertable(self, n_list):
      self.fingerTable = n_list
      self.showFingertable(self.fingerTable)

    def getNodeSucc(self):
      if not self.fingerTable:
        raise SystemException("Error: No successors, fingertable empty!")
      return self.fingerTable[0]

    '''
    Returns: True if key_1 is after key_2 in clockwise order, False otherwise.
    Params: key_1 (int) - integer representing sha-256 hash
    Params: key_2 (int) - integer representing sha-256 hash
    '''
    def contains(self, item, lower_bound, upper_bound):
      case_1 = (lower_bound < item and item < upper_bound)
      case_2 = (item < upper_bound and upper_bound < lower_bound)
      case_3 = (upper_bound < lower_bound and lower_bound < item)

      return case_1 or case_2 or case_3

    def findPred(self, key):
      if not self.fingerTable:
        raise SystemExcetion("Error: No predecessors, fingertable empty!")

      closest_node = None

      for i in range(len(self.fingerTable)-1, -1, -1):
        if(self.contains(int(self.fingerTable[i].id, 16),\
                         int(self.myNode.id, 16),\
                         int(key, 16))):
          closest_node = self.fingerTable[i]

          transport = TSocket.TSocket(closest_node.ip, str(closest_node.port))
          # Buffering is critical. Raw sockets are very slow
          transport = TTransport.TBufferedTransport(transport)
          # Wrap in a protocol
          protocol = TBinaryProtocol.TBinaryProtocol(transport)
          # Create a client to use the protocol encoder
          client = FileStore.Client(protocol)
          transport.open()

          return client.findPred(key)
          break

      return self.myNode

    def findSucc(self, key):
      if not self.fingerTable:
        raise SystemException("Error: No fingertable!")

      pred = self.findPred(key)

      if pred == self.myNode:
        return self.fingerTable[0]

      ## Find predecessor
      transport = TSocket.TSocket(pred.ip, str(pred.port))
      # Buffering is critical. Raw sockets are very slow
      transport = TTransport.TBufferedTransport(transport)
      # Wrap in a protocol
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      # Create a client to use the protocol encoder
      client = FileStore.Client(protocol)
      transport.open()

      return client.getNodeSucc()

if __name__ == '__main__':
    port_num = int(sys.argv[1])
    handler = ChordHandler()
    processor = FileStore.Processor(handler)
    transport = TSocket.TServerSocket(port=port_num)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    try:
      print('Starting the server...')
      server.serve()
      print('done.')
    except KeyboardInterrupt:
      transport.close()
