#!/usr/bin/python

import os, time, sys, types, copy, cStringIO, threading
import urllib, urllib2, socket, select, shutil
import paramiko

class Server:
    def process_request_Thread(self, request, client_address):
        try:
            
	    print "\n\n+++ GOT CONNECT FROM: " + client_address[0]	
            request.send("\nSend me a username (50 characters max please):")   
            chunk = request.recv(50)
              

            if chunk == '':
              raise RuntimeError, "socket connection broken"
	    username = ''.join(e for e in chunk if e.isalnum())	

            print "     --- USERNAME: '" + username + "'"
               

            request.send("\nI'm seeing: " + username)
           
	    request.send("\nI'm going to wait for 45 seconds and tell you now... guessing won't work\n")
	    time.sleep(45)
            request.send("\nSend me a password (50 characters max please):")   
            chunk = request.recv(50)
              

            if chunk == '':
              raise RuntimeError, "socket connection broken"
            
            password = ''.join(e for e in chunk if e.isalnum())

	    print "     --- PASSWORD: '" + password + "'"
            
            

            request.send("\nI'm seeing: " + password)
            
            request.send("\nWait by the phone...\n\n\n\n")

            request.shutdown(2)     # apachebench needs this, weird...

            request.close()

	    print "     --- Waiting 10 seconds"
	    time.sleep(10)

        except Exception,x:

            print "     --- Error during connection: %s" % x

	try:
	    client = paramiko.SSHClient()
	    client.load_system_host_keys()
	    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	    print '    ---  Connecting: ' + client_address[0]
	    client.connect(client_address[0], 22, username, password)
#	    chan = client.invoke_shell()
	    print repr(client.get_transport())
	    print '    *** Here we go!'
	    print
#	    interactive.interactive_shell(chan)
	    stdin, stdout, sterr = client.exec_command("echo BLAHBLAHBLAHTHISISNOTTHEKEY > seedfile.txt")
	    stdin, stdout, sterr = client.exec_command("sh -c \"echo '#!/bin/bash' > script.sh\"")	
	    stdin, stdout, sterr = client.exec_command("sh -c \"echo 'sha512sum seedfile.txt | base64 | base64 | base64 | base64 | md5sum'  >> script.sh\"")
	    stdin, stdout, sterr = client.exec_command("sh -c \"chmod 700 script.sh\"")
	    stdin, stdout, sterr = client.exec_command("sh -c \"./script.sh\"")
	    stdin, stdout, sterr = client.exec_command("base64 ./script.sh > AsCrIpT64U")
	    stdin, stdout, sterr = client.exec_command("rm -f ./script.sh")
#	    chan.close()
	    client.close()

	except Exception, e:
	    print '*** Caught exception: %s: %s' % (e.__class__, e)
#	    traceback.print_exc()
	    try:
	      client.close()
	    except:
	      pass
	    
  
  
  
  
  
  
  
  
  

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

                request.shutdown(2)     # apachebench needs this, weird...

                request.close()

            except Exception,x:

                print "Error during closing of connection: %s" % x

  

    def serve_forever(self):

        

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(("localhost", 9091))

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
