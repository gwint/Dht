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

  assert client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83").port == 9000
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

  assert client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83").port == 9000
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

  assert client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83").port == 9000
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

  res = client.findPred("42E197B31EF421E4B7995324FD8FA7CE9F781E32002C65BA86DBABADE24AEC83")
  print res.port
  assert res.port == 9000
  print "findPred() test 4 passed"

  transport.close()


def main():
    # Make socket
#    transport = TSocket.TSocket('alpha.cs.binghamton.edu', 9000)
    # Buffering is critical. Raw sockets are very slow
#    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
#    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
#    client = FileStore.Client(protocol)
    # Connect!
#    transport.open()

#    meta_obj = RFileMetadata()
#    meta_obj.filename = "book.txt"
#    meta_obj.version = 0
#    meta_obj.owner = "Brad"
#    meta_obj.contentHash = hashlib.sha256(meta_obj.filename +\
#                            ":" + meta_obj.owner).hexdigest()

#    content_str = "Knowledge Bitch!"
#    file_obj = RFile()
#    file_obj.meta = meta_obj
#    file_obj.content = content_str

    ## Test findPred()
#    key_2 = "CE5B56C3815D692CA036D6A663DCB29683481756C201B6EF50A7E8F4D8532022"
#    key_3 = "60DE97FE3C29E0EC465924E8CDE1189BF29F73D03495B1E1740A3D10A407FFDD"
#    key_4 = "445BE48D4D32D4F22B278A424A430CD533BB5E8D80F5C0B85289D1DFE6A328EA"

    ##client.writeFile(file_obj)
#    key = "42e197b31ef421e4b7995324fd8fa7ce9f781e32002c65ba86dbabade24aec83"
##    print(client.findPred(key))
    testPred1()
    testPred2()
    testPred3()
    testPred4()
    # Close!
#    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
