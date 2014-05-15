#!/usr/bin/python

import struct
import sys
import random
import time

def handshake() :
  sys.stdout.write("HeyBotYouThere")
  sys.stdout.flush()
  x = sys.stdin.read(4)
  sys.stderr.write("shake1 got " + repr(x))
  if x != "Yeah" :
    return False
  sys.stdout.write("YouReady")
  sys.stdout.flush()
  x = sys.stdin.read(24)
  sys.stderr.write("shake2 got " + repr(x))
  if x != "HeckYeahIWantCheezyPoofs" :
    return False
  else :
    return True
  


def dothemath(a, b, op) :
	
	if op == 0x01 :
		return struct.pack("I", (a + b))
	if op == 0x29 :
		return struct.pack("I", (a - b))
#0x31 XOR
	if op == 0x31 :
		return struct.pack("I", (a ^ b))
	if op == 0x21 :
		return struct.pack("I", (a & b))
	if op == 0x09 :
		return struct.pack("I", (a | b))
	return 0

def outputpacket(a, b, op, roundn) :

#	sys.stdout.write(struct.pack("bIII", op, a, b, roundn))
	sys.stdout.write(struct.pack("b", 14))
	sys.stdout.write(struct.pack("b", op))
	sys.stdout.write(struct.pack(">I", a))
	sys.stdout.write(struct.pack("<I", b))
	sys.stdout.write(struct.pack("I", roundn))
	sys.stdout.flush()


	

def doround(roundn, op=65535) :
	
	if op == 65535 :
		op = random.choice([0x01,0x29])
	if op == 65534 :
		op = random.choice([0x01,0x29, 0x31, 0x21, 0x09])
	
	if op == 0x01 :
                term1 = random.randint(1,0xFFFFFFFF)
		term2 = random.randint(1,(0xFFFFFFFF - term1))
		sys.stderr.write( str(term1) + " + " + str(term2) +"\n" )
		outputpacket(term1, term2, op, roundn)
		
        if op == 0x29 :

		term1 = random.randint(3,0xFFFFFFF)
		term2 = random.randint(1,(term1 - 1))
		sys.stderr.write( str(term1) + " - " + str(term2) +"\n" )
		outputpacket(term1, term2, op, roundn)

	if op == 0x31 :
                term1 = random.randint(1,0xFFFFFFFF)
		term2 = random.randint(1,0xFFFFFFFF)
		sys.stderr.write( str(term1) + " ^ " + str(term2) +"\n" )
		outputpacket(term1, term2, op, roundn)
	if op == 0x21 :
                term1 = random.randint(1,0xFFFFFFFF)
		term2 = random.randint(1,0xFFFFFFFF)
		sys.stderr.write( str(term1) + " & " + str(term2) +"\n" )
		outputpacket(term1, term2, op, roundn)	
	if op == 0x09 :
                term1 = random.randint(1,0xFFFFFFFF)
		term2 = random.randint(1,0xFFFFFFFF)
		sys.stderr.write( str(term1) + " | " + str(term2) +"\n" )
		outputpacket(term1, term2, op, roundn)
	x = sys.stdin.read(4)
	if x == dothemath(term1, term2, op) :
	  
	  return True
	else :
	  print repr(x) + "wrong"
	  sys.stderr.write(repr(x) + "wrong")
	  return False

if __name__ == "__main__":
  
  if not handshake() :
    print "bad shake"
    sys.exit(1)
	   
  for  i in range(1, 51) : 
    time.sleep(1)
    sys.stderr.write("\n\n round : " + str(i) + " " )
    if not doround(i) :
	  sys.exit(1)
  for i in range(51,101) :
    time.sleep(1)
    sys.stderr.write("\n\n round : " + str(i) + " " )
    if not doround(i, 65534) :
      sys.exit(1)
  sys.stdout.write(struct.pack("b", 39))
  sys.stdout.write("key={7cc50be839881287d586379025c67eb1}") 
  sys.stdout.flush()	  
