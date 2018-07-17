from subprocess import call, Popen

import socket
import sys
from thread import *
from time import strftime, gmtime
import os.path
import time

SERVER_NAME = "Greg's Server"

host = ''
port = 9999

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    global port
    s.bind((host, port))
  except socket.error as e:
    print(str(e))

  s.listen(5)

  print("Waiting for connections")

  try:
    while True:
      conn, addr = s.accept()
      for port in range(19000, 19004):
        Popen(["python", "server.py"] + [str(port)])

      ## Create nodes.txt

      ## Initalize dht
  except KeyboardInterrupt:
    s.shutdown(socket.SHUT_RDWR)
    s.close()


main()
