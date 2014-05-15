#!/usr/bin/python
#target = "128.238.66.221"
target = "107.170.157.24"
targetport = 7337

import sys, socket, select
import struct

def handshake(s) :
  x = s.recv(20)
  s.send("Yeah")
  x = s.recv(20)
  s.send("HeckYeahIWantCheezyPoofs")

def dothemath(a, b, op) :
	
	if op == 0x01 :
		print a+b
		return struct.pack("I", (a + b))
	if op == 0x29 :
		print a-b
		return struct.pack("I", (a - b))
#0x31 XOR
	if op == 0x31 :
		return struct.pack("I", (a ^ b))
	if op == 0x21 :
		return struct.pack("I", (a & b))
	if op == 0x09 :
		return struct.pack("I", (a | b))
	return 0

def connecttoserver() :
  s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  connect=s.connect((target,targetport))
  return s

def clientround(s) :
  received = s.recv(100)
  print repr(received)
#problem=struct.unpack("bIII", received)

  op = struct.unpack("b",received[1])
  term1 = struct.unpack(">I",received[2:6])
  term2 = struct.unpack("<I",received[6:10])
  print repr(op) + " " + repr(term1) + " " + repr(term2)
  result=dothemath(term1[0],term2[0],op[0])
  print repr(result)
  s.send(result)
  
if __name__ == "__main__":
  
  handle = connecttoserver()
  handshake(handle)
  while True :
    clientround(handle)
    
