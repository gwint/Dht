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

import sys
import glob
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/usr/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import RFile, RFileMetadata, NodeID, SystemException

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import hashlib

NODE_INFO_FILE = "nodes.txt"

def run_succ_tests(host, port_list):
  def testSucc(query_port):
    # Make socket
    transport = TSocket.TSocket(host, query_port)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = FileStore.Client(protocol)
    # Connect!
    transport.open()

    for port in port_list:
      hash = \
        hashlib.sha256(("%s:%d" % (host, port)).encode("utf-8")).hexdigest()
      decremented_hash_str = hex(int(hash, 16) - 1)[2:]
      assert client.findSucc(decremented_hash_str).id == hash

    print("findSucc(%d) test passed" % query_port)
    transport.close()

  for port in port_list:
    testSucc(port)

def run_pred_tests(host, port_list):
  def testPred(query_port):
    # Make socket
    transport = TSocket.TSocket(host, query_port)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = FileStore.Client(protocol)
    # Connect!
    transport.open()

    for port in port_list:
      hash = hashlib.sha256(("%s:%d" % (host, port)).encode("utf-8")).hexdigest()
      incremented_hash_str = hex(int(hash, 16) + 1)[2:]
      assert client.findPred(incremented_hash_str).id == hash

    print("findPred(%d) test passed" % query_port)
    transport.close()

  for port in port_list:
    testPred(port)

def testReadAfterWrite():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  meta_obj = RFileMetadata()
  meta_obj.filename = "book.txt"
  meta_obj.version = 0
  meta_obj.owner = "Brad"
  meta_obj.contentHash = hashlib.sha256(meta_obj.filename +\
                              ":" + meta_obj.owner).hexdigest()

  content_str = "Knowledge Bitch!"
  file_obj = RFile()
  file_obj.meta = meta_obj
  file_obj.content = content_str

  client.writeFile(file_obj)

  transport.close()

  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  res = client.readFile("book.txt", "Brad")

  print("Read after write successful")

  transport.close()

def testReadAfterWriteError():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  meta_obj = RFileMetadata()
  meta_obj.filename = "book.txt"
  meta_obj.version = 0
  meta_obj.owner = "Brad"
  meta_obj.contentHash = hashlib.sha256(meta_obj.filename +\
                              ":" + meta_obj.owner).hexdigest()

  content_str = "Knowledge Bitch!"
  file_obj = RFile()
  file_obj.meta = meta_obj
  file_obj.content = content_str

  client.writeFile(file_obj)

  transport.close()

  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9001)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  try:
    res = client.readFile("book.txt", "Brad")
    print("Read after write error NOT succesful")
  except SystemException:
    print("Read after write error successful")

  transport.close()


def incorrectOwnerTest():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  meta_obj = RFileMetadata()
  meta_obj.filename = "book.txt"
  meta_obj.version = 0
  meta_obj.owner = "Brad"
  meta_obj.contentHash = hashlib.sha256(meta_obj.filename +\
                              ":" + meta_obj.owner).hexdigest()

  content_str = "Test String"
  file_obj = RFile()
  file_obj.meta = meta_obj
  file_obj.content = content_str

  client.writeFile(file_obj)

  transport.close()

  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  try:
    res = client.readFile("book.txt", "Drake")
  except SystemException:
    print("Success: Incorrect owner")

  transport.close()

def testOverwrite():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  meta_obj = RFileMetadata()
  meta_obj.filename = "book.txt"
  meta_obj.version = 0
  meta_obj.owner = "Brad"
  meta_obj.contentHash = hashlib.sha256(meta_obj.filename +\
                              ":" + meta_obj.owner).hexdigest()

  content_str = "Test String"
  file_obj = RFile()
  file_obj.meta = meta_obj
  file_obj.content = content_str

  client.writeFile(file_obj)

  transport.close()

  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  file_obj.meta.version = file_obj.meta.version + 1
  file_obj.content = "New Test String"

  client.writeFile(file_obj)

  try:
    # Make socket
    transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = FileStore.Client(protocol)
    # Connect!
    transport.open()

    res = client.readFile("book.txt", "Brad")
    assert res.content == "New Test String"
    assert res.meta.version == 1
    print("File Overwrite Successful")

  except SystemException:
    print("Success: Incorrect owner")

  transport.close()

def main():
  port_list = []
  node_file_obj = open(NODE_INFO_FILE, 'r')
  conn_tuple = node_file_obj.readline().strip()
  host = conn_tuple.split(':')[0]
  while conn_tuple:
    peices = conn_tuple.split(':')
    host = peices[0]
    port = int(peices[1])
    port_list.append(port)
    conn_tuple = node_file_obj.readline().strip()

  run_pred_tests(host, port_list)
  run_succ_tests(host, port_list)
  #testOverwrite()
  #testReadAfterWrite()
  #testReadAfterWriteError()
  #incorrectOwnerTest()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
