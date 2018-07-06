#!/usr/bin/env python

#
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
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import NodeID, RFile, RFileMetadata, SystemException
#from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from socket import gethostbyname, gethostname

import init
import hashlib

import logging
logging.basicConfig(level=logging.DEBUG)


class ChordHandler:
    def __init__(self):
        #self.log = {}
        #entry = SharedStruct()
        #entry.key = 311995
        #entry.value = '%d' % (23)
        #self.log[entry.key] = entry
        self.fingerTable = []
        self.contentHashes = []
        self.myNode = NodeID()
        port = int(sys.argv[1])
        ipAddr = gethostbyname(gethostname())
        idStr = gethostbyname(gethostname()) + ":" + sys.argv[1]
        #print idStr
        key = hashlib.sha256(idStr).hexdigest()
        #print int(key, 16)
        self.myNode.ip = ipAddr
        self.myNode.port = port
        self.myNode.id = key
        #print(self.myNode)
        self.fileData = []

##    def ping(self):
##        print('ping()')

##    def getStruct(self, key):
##        print('getStruct(%d)' % (key))
##        return self.log[key]

##    def zip(self):
##        print('zip()')

    def writeFile(self, file_obj):
      file_name = file_obj.meta.filename
      #print("file_name: %s" % file_name)

      succ = self.findSucc(file_obj.meta.contentHash)
      #print("succ id: ", succ.id)
      #print("my id: ", self.myNode.id)
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
      ## TODO::FIX
      succ = self.findSucc(hash)
      #print("succ id: ", succ.id)
      #print("my id: ", self.myNode.id)
      if(succ.id != self.myNode.id):
        raise SystemException("Cannot Read: Server does not own this file!")

      for obj in self.fileData:
        if obj.meta.contentHash == hash:
          return obj
      raise SystemException("Hash not found: Check owner or file name!")

    def setFingertable(self, n_list):
      self.fingerTable = n_list
      #i = 0
      #for row in self.fingerTable:
      #  print("%d: %d" % (i, row.port))
      #  i += 1

    def getNodeSucc(self):
      if not self.fingerTable:
        raise SystemException("Error: No successors, fingertable empty!")
      return self.fingerTable[0]

    def findPred(self, key):
      #print(int(self.myNode.id, 16))
      succNode = self.getNodeSucc()
      if not self.fingerTable:
        raise SystemExcetion("Error: No predecessors, fingertable empty!")
      if(self.fingerTable[0].id == self.myNode.id):
        return self.myNode
      if (((key < succNode.id) and (self.myNode.id > succNode.id or\
                                  self.myNode.id < key)) or\
          (key > self.myNode.id and key > succNode.id and\
          self.myNode.id > succNode.id)) or key == self.myNode.id:
        #print "I am the predecessor"
        return self.myNode
      else:
        #print "Must make rpc"
        i = 0
        currNode = self.myNode
        nextNode = self.getNodeSucc()
        #print "key: ", int(key, 16)

        #part_1 = key < nextNode.id and ((currNode.id > nextNode.id) or\
        #                                self.myNode.id < key))

        a = key < nextNode.id
        b = (currNode.id > nextNode.id) or (currNode.id < key)
        c = (key > currNode.id) and\
            (key > nextNode.id) and\
            (currNode.id > nextNode.id)

        d = a and b
        e = d or c

#        while (not ((key < nextNode.id) and (currNode.id > nextNode.id or\
#                                  currNode.id < key)) or\
#                   (key > currNode.id and key > nextNode.id and\
#                    currNode.id > nextNode.id)) and i < len(self.fingerTable) and\
#                   (self.fingerTable[i].id != self.myNode.id):
        while (not e) and i < len(self.fingerTable) and\
                   (self.fingerTable[i].id != self.myNode.id):

            #print "currNode: ", int(currNode.id, 16)
            #print "nextNode: ", int(nextNode.id, 16)

            currNode = self.fingerTable[i]
            #print "new currNode: ", int(currNode.id, 16)

            transport = \
               TSocket.TSocket(currNode.ip, str(currNode.port))
            # Buffering is critical. Raw sockets are very slow
            transport = TTransport.TBufferedTransport(transport)
            # Wrap in a protocol
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            # Create a client to use the protocol encoder
            client = FileStore.Client(protocol)
            transport.open()

            nextNode = client.getNodeSucc()
            i += 1

            a = key < nextNode.id
            b = (currNode.id > nextNode.id) or (currNode.id < key)
            c = (key > currNode.id) and\
                (key > nextNode.id) and\
                (currNode.id > nextNode.id)

            d = a and b
            e = d or c


        #print(currNode)
        #print(self.myNode)
        ##if currNode == self.myNode:
        ##  return currNode
        ##else:
          ## make rpc to currNode
          # Make socket
        #print "my_ip: ", self.myNode.ip
        #print "my_port: ", self.myNode.port
        #print "target_ip: ", currNode.ip
        #print "target_port: ", currNode.port
        transport = TSocket.TSocket(currNode.ip, str(currNode.port))
        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # Create a client to use the protocol encoder
        client = FileStore.Client(protocol)
        transport.open()
        pred = client.findPred(key)
        return pred

    def findSucc(self, key):
      if not self.fingerTable:
        raise SystemException("Error: No fingertable!")

      if key == self.myNode.id:
        return self.myNode

      pred = self.findPred(key)
      succ = self.fingerTable[0]

      if pred.id == key:
        return pred

      if pred.id != self.myNode.id:
        transport = TSocket.TSocket(pred.ip, str(pred.port))
        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)
        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # Create a client to use the protocol encoder
        client = FileStore.Client(protocol)
        transport.open()

        succ = client.getNodeSucc()

      return succ

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

    print('Starting the server...')
    server.serve()
    print('done.')
