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

def main():
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
    ##client.writeFile(file_obj)
    key = "42e197b31ef421e4b7995324fd8fa7ce9f781e32002c65ba86dbabade24aec83"
    print(client.findPred(key))
    # Close!
    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
