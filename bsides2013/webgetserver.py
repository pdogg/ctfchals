#!/usr/bin/python

import os, time, sys, types, copy, cStringIO, threading
import socket, select, shutil, binascii
import string, requests


WAIT = 1

keyspace = string.ascii_letters + string.digits

def slicen(s, n, truncate=False):
	    assert n > 0
	    while len(s) >= n:
		yield s[:n]
		s = s[n:]
	    if len(s) and not truncate:
	        yield s


def hexdelimit(string):
	outstring = ""
        hexstring = binascii.b2a_hex(string)
	for byte in slicen(hexstring, 2):
		outstring += "\\x" + byte
	return outstring
	
def encrypt(plain, key):
	return base64.b64encode(plain)

def decrypt(cipher, key):
	return base64.b64decode(cipher)

		  



class Server:
    def process_request_Thread(self, request, client_address):
        try:
            
	    print "\n\n+++ GOT CONNECT FROM: " + client_address[0]	
            request.send("\nPick a number from 1-65535: ")   
            chunk = request.recv(50)
              

            if chunk == '':
              raise RuntimeError, "socket connection broken"
	    remoteport = ''.join(e for e in chunk if e.isalnum())	

	    print "--- PORT NUMBER SENT: " + remoteport
               

            request.send("\nI'm seeing: " + remoteport)
            try:
		remoteportnum = int(remoteport)
	    except:
		request.send("\nYou probably didn't send me a number like I asked! Play nice!\n")
                request.close
		return False
	   
	    if remoteportnum > 65535 or remoteportnum < 1:
		request.send("\n1-65535 ... " + str(remoteportnum) + " try again...\n")
		request.close
		return False
            request.send("\nI'm going to wait for " + str(WAIT) + " seconds and tell you brute force has nothing to do with this\n")
	    time.sleep(WAIT)
	    request.send("\nGive me something to get: ")   
	    chunk = request.recv(50)           

	    if chunk == '':
	      raise RuntimeError, "socket connection broken"
	    remotefile = chunk	    
	    print "--- REMOTE FILE SENT: " + remotefile
											               

	    request.send("\nI'm seeing: " + remotefile)


            request.send("\nWait a few seconds...\n\n\n\n")

            request.shutdown(2) 

            request.close()

	    print "--- Waiting " + str(WAIT) + " seconds"
	    time.sleep(WAIT)
	    
	    url = "http://" + client_address[0] + ":" + str(remoteport) + "/" + remotefile.strip()

	    print "Connecting : " + client_address[0] + " " + str(remoteport)
	    print url

	    r = requests.get(url)
	    if r.status_code < 400:
		   cookies = dict(the_key_is="blahblah")
		   r = requests.get(url, cookies=cookies)

        except Exception,x:

            print "     --- Error during connection: %s" % x

    def handle_request(self):
        # Handle one request, possibly blocking.
        try:
            request, client_address = self.socket.accept()
        except socket.error:
            return
        try:
            t = threading.Thread(target = self.process_request_Thread, args = (request, client_address))
            t.setDaemon(False)
            t.start()
           

        except:
            try:
                request.shutdown(2)    
                request.close()

            except Exception,x:
                print "Error during closing of connection: %s" % x

  

    def serve_forever(self):


        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("0.0.0.0", 9091))
        self.socket.listen(100)     # start listening on the socket
        self.mustShutdown=False
        

        previousReap=time.time()
        while not self.mustShutdown:
            ins,outs,excs=select.select([self],[],[self],10)    # 10 second timeout
            if self in ins:
                self.handle_request()

        

    def fileno(self):
	    # interface required for select system call

        return self.socket.fileno()


Server().serve_forever()
