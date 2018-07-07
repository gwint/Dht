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
        self.fingerTable = []
        self.contentHashes = []
        self.myNode = NodeID()
        port = int(sys.argv[1])
        ipAddr = gethostbyname(gethostname())
        idStr = gethostbyname(gethostname()) + ":" + sys.argv[1]
        key = hashlib.sha256(idStr).hexdigest()
        self.myNode.ip = ipAddr
        self.myNode.port = port
        self.myNode.id = key
        self.fileData = []

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

    def getNodeSucc(self):
      if not self.fingerTable:
        raise SystemException("Error: No successors, fingertable empty!")
      return self.fingerTable[0]

    def findPred(self, key):
      succNode = self.getNodeSucc()
      if not self.fingerTable:
        raise SystemExcetion("Error: No predecessors, fingertable empty!")
      return None

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
