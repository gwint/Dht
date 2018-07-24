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
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import RFile, RFileMetadata, NodeID, SystemException

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import hashlib

## Must look in nodes.txt to get ports being used
## Controller.py is going to create nodes.txt which will be read here

def testSucc1():
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

  res_1 = client.findSucc("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC81")
  res_2 = client.findSucc("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532021")
  res_3 = client.findSucc("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDC")
  res_4 = client.findSucc("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328E9")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findSucc() test 1 passed"
  transport.close()

def testSucc2():
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

  res_1 = client.findSucc("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC81")
  res_2 = client.findSucc("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532021")
  res_3 = client.findSucc("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDC")
  res_4 = client.findSucc("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328E9")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findSucc() test 2 passed"
  transport.close()

def testSucc3():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9002)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  res_1 = client.findSucc("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC81")
  res_2 = client.findSucc("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532021")
  res_3 = client.findSucc("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDC")
  res_4 = client.findSucc("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328E9")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findSucc() test 3 passed"
  transport.close()

def testSucc4():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9003)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  res_1 = client.findSucc("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC81")
  res_2 = client.findSucc("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532021")
  res_3 = client.findSucc("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDC")
  res_4 = client.findSucc("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328E9")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findSucc() test 4 passed"
  transport.close()

def testPred1():
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

  key_1 = "42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC82"

  res_1 = client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83")
  res_2 = client.findPred("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532023")
  res_3 = client.findPred("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDE")
  res_4 = client.findPred("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328EC")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findPred() test 1 passed"

  transport.close()

def testPred2():
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

  key_1 = "42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC82"

  res_1 = client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83")
  res_2 = client.findPred("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532023")
  res_3 = client.findPred("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDE")
  res_4 = client.findPred("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328EC")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findPred() test 2 passed"

  transport.close()

def testPred3():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9002)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  key_1 = "42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC82"

  res_1 = client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83")
  res_2 = client.findPred("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532023")
  res_3 = client.findPred("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDE")
  res_4 = client.findPred("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328EC")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003

  print "findPred() test 3 passed"

  transport.close()

def testPred4():
  # Make socket
  transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9003)
  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)
  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # Create a client to use the protocol encoder
  client = FileStore.Client(protocol)
  # Connect!
  transport.open()

  key_1 = "42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC82"

  res_1 = client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83")
  res_2 = client.findPred("CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532023")
  res_3 = client.findPred("60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDE")
  res_4 = client.findPred("445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328EC")

  assert res_1.port == 9000
  assert res_2.port == 9001
  assert res_3.port == 9002
  assert res_4.port == 9003
  print "findPred() test 4 passed"

  transport.close()

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

  print "Read after write successful"

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
    print "Read after write error NOT succesful"
  except SystemException:
    print "Read after write error successful"

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
    print "Success: Incorrect owner"

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
    print "File Overwrite Successful"

  except SystemException:
    print "Success: Incorrect owner"

  transport.close()


def main():
  testPred1()
  testPred2()
  testPred3()
  testPred4()

  testSucc1()
  testSucc2()
  testSucc3()
  testSucc4()

  testOverwrite()
  testReadAfterWrite()
  testReadAfterWriteError()
  incorrectOwnerTest()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
