#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        
        method = self.data.split()[0]
        path = self.data.split()[1] 

        if method[:3] != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))

        else:
            if ".." in path:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            
            elif path[-1] == '/':
                fullpath = os.getcwd() + "/www" + path + "index.html"
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf=8'))
                    return
                self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(f)}\r\n\r\n{f}", 'utf-8'))
            
            elif path[-5:] == ".html":
                fullpath = os.getcwd() + "/www" + path
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf=8'))
                    return
                self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(f)}\r\n\r\n{f}", 'utf-8'))
            
            elif path[-4:] == ".css":
                fullpath = os.getcwd() + "/www" + path
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf=8'))
                    return
                self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: {len(f)}\r\n\r\n{f}", 'utf-8'))
            
            else:
                fullpath = os.getcwd() + "/www" + path + "/index.html"
                try:
                    file = open(fullpath)
                    f = file.read()
                    file.close()
                except:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", 'utf-8'))
                    return
                self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\r\nLocation: {path}/\r\n",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
