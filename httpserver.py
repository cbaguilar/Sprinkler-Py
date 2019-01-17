import time
import atexit
import socket
import sys
import threading
import json
import datetime
import Fake.GPIO as gp

import SocketServer
import ssl
import BaseHTTPServer
import os

now = datetime.datetime.now()
today = datetime.datetime.today()
HOST = None               
PORT = 8000
s = None
SCHEDULE_FILE = "program"

global_schedule_object =  json.load(open(SCHEDULE_FILE)) #JSON program object


def reload_schedule():
	global_schedule_object =  json.load(open(SCHEDULE_FILE)) 
	
def load_local_schedule_string():
	return(open(SCHEDULE_FILE))


def send_schedule(s):
	s.send_response(200)
	s.send_header("Content-type","text/html")
	s.end_headers()
	s.wfile.write(" "+json.dumps(global_schedule_object, sort_keys=True, 
						indent=4))
		

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		reload_schedule()
		uri = s.path
		if uri == "/schedule":
			print("sendigng schedule")
			send_schedule(s)
			
		
		
if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(("", 8000), MyHandler)
	try:
		httpd.serve_forever()
	except KeyBoardInterrupt:
		pass
	http.server_close()
