# Echo server program
import time
import atexit
import socket
import sys
import threading
import json
import datetime
import Rpi.GPIO as gp

print("changed from github")

now = datetime.datetime.now()

HOST = None               # Symbolic name meaning all available interfaces
PORT = input("Enter Port")              # Arbitrary non-privileged port
s = None


file = open("program","r")
program = file.read()
print(program)
file.close()

Oprogram = json.loads(program)


'''
~~~~~EPIC SERVER MESSAGE LIST!!!~~~~~
I will make a list of different messages/commands here.

get-file x   send_file(x)       sends the current program to the client
update       recieve_file()     starts receving new file from the client
disconnect   close()            closes connecton
force-on x   force_ctrl(x,T/F)  direct control sprinkler x on/off
rename x name rename(x,name)    renames sprinkler x to name

'''





def str2bool(v):
  return v.lower() in ("true")


def newsprink(sprinkler):
    if sprinkler == 1:
        gp.setup(3,0)
    elif sprinkler == 2:
        gp.setup(5,0)
    elif sprinkler == 3:
        gp.setup(7,0)
    elif sprinkler == 4:
        gp.setup(11,0)
    elif sprinkler == 5:
        gp.setup(13,0)
    elif sprinkler == 6:
        gp.setup(15,0)
    elif sprinkler == 7:
        gp.setup(19,0)
    elif sprinkler == 8:
        gp.setup(21,0)
    elif sprinkler == 9:
        gp.setup(23,0)
    elif sprinkler == 10:
        gp.setup(22,0)
    elif sprinkler == 11:
        gp.setup(24,0)
    elif sprinkler == 12:
        gp.setup(26,0)
def sprinkler(sprinkler, on):
    
    #numbering sprinklers by column
    if sprinkler == 1:
        gp.output(3,on)
    elif sprinkler == 2:
        gp.output(5,on)
    elif sprinkler == 3:
        gp.output(7,on)
    elif sprinkler == 4:
        gp.output(11,on)
    elif sprinkler == 5:
        gp.output(13,on)
    elif sprinkler == 6:
        gp.output(15,on)
    elif sprinkler == 7:
        gp.output(19,on)
    elif sprinkler == 8:
        gp.output(21,on)
    elif sprinkler == 9:
        gp.output(23,on)
    elif sprinkler == 10:
        gp.output(8,on)
    elif sprinkler == 11:
        gp.output(10,on)
    elif sprinkler == 12:
        gp.output(12,on)

    print("Set sprinkler "+sprinkler+" to "+on)
    #conn.send("Set sprinkler "+sprinkler+" to "+on"\n)	


def sprinkler(sprinkler, on):
    
    #numbering sprinklers by column
    if sprinkler == 1:
        gp.output(3,on)
    elif sprinkler == 2:
        gp.output(5,on)
    elif sprinkler == 3:
        gp.output(7,on)
    elif sprinkler == 4:
        gp.output(11,on)
    elif sprinkler == 5:
        gp.output(13,on)
    elif sprinkler == 6:
        gp.output(15,on)
    elif sprinkler == 7:
        gp.output(19,on)
    elif sprinkler == 8:
        gp.output(21,on)
    elif sprinkler == 9:
        gp.output(23,on)
    elif sprinkler == 10:
        gp.output(8,on)
    elif sprinkler == 11:
        gp.output(10,on)
    elif sprinkler == 12:
        gp.output(12,on)

    print("Set sprinkler "+sprinkler+" to "+on)
    #conn.send("Set sprinkler "+sprinkler+" to "+on"\n)
    
    
    

    
def initialize():
    print "Initializing"
    gp.setmode(gp.BOARD)
    print ("Set up board")
    gp.setup(3,gp.OUT)
    gp.setup(5,gp.OUT)
    gp.setup(7,gp.OUT)
    gp.setup(11,gp.OUT)
    gp.setup(13,gp.OUT)
    gp.setup(15,gp.OUT)
    gp.setup(19,gp.OUT)
    gp.setup(21,gp.OUT)
    gp.setup(23,gp.OUT)
    gp.setup(8,gp.OUT)
    gp.setup(10,gp.OUT)
    gp.setup(12,gp.OUT)
    print "Set up pins"
    

    
def server_thread():

    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = NoneW
            continue
        try:
            s.bind(sa)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            s.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
 
    if s is None:
	
        print 'could not open socket'
        sys.exit(1)
    while 1:
  	  conn, addr = s.accept()
 	  print 'Connected by', addr
	  conn.send(program+'\n')
	  while 1:
	         data = conn.recv(4096)
       		 print(data)
       		 conn.send(data+"\n")
		 try:	
		
	         	print("wrote new file file")
			Oprogram = json.loads(data)
			if Oprogram["type"] == "program":
				file = open("program","w")
				file.write(json.dumps(Oprogram["program"]))
				print(Oprogram["program"]["times"][1])
				file.close()
				Oprogram = Oprogram["program"]
		 except Exception, e1:
			print str(e1)
       	   	 if not data: break
       
    conn.close()


def sprinkler_thread():
     while 1:
     	lfile = open("program","r")
     	Oprogram = json.loads(lfile.read())
        now = datetime.datetime.now()
        if int(Oprogram["start"]) == now.hour:
                
        	print("Started Program")
        	for x in range (0,12):
	                lfile = open("program","r")
	       		Oprogram = json.loads(lfile.read())
	       		cs = x+1
                	wait = Oprogram["times"][x]
                        print("Started Sprinkler "+str(cs)+" for "+str(wait))
                        newsprink(x)
                        time.sleep(float(wait*60))
                        gp.cleanup()
                        
                print("Finished program, waiting for hour to end")
        else:
        	print("Not time yet, time set to ",Oprogram["start"])
        time.sleep(10)


try:
	
   	serv = threading.Thread(target=server_thread)
	sprink = threading.Thread(target=sprinkler_thread)
	sprink.daemon= True
	serv.daemon = True
	sprink.start()
	serv.start()
	#sleep(1)
   	# if Oprogram["start"] ==now.Hour:

except Exception, e:
    print "Error: Could not start thread"
    print str(e)
    ##file.close()        
while 1:
	ipt = raw_input("--> ")
	if ipt == "stop":
		gp.cleanup()
		try:
			conn.close()
		except:
			print("teehee")
		sys.exit()
    	pass

