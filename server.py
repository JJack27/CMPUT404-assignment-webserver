#  coding: utf-8 
import socketserver
import time
import mimetypes
# ==============================================
# Copyright 2019 Yizhou Zhao

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =====================================================
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

        # receiving requests
        self.data = self.request.recv(1024).strip()
        
        # getting the first line of HTTP requests
        method_line = self.data.decode().split("\r\n")[0]
        method_type, address, _ = method_line.split(" ")

        address = "./www" + address
        # check if its a GET request
        if (method_type == "GET"):
            header = ""
            page = ""
            try:
                # add "index.html" to the end of address if it ends with "/"
                
                if (address[-1] == "/"):
                    address += "index.html"
                # define the header. Status code and mime type
                header = "HTTP/1.1 200 OK\r\nContent-Type: "
                mime_type = mimetypes.types_map["." + address.split(".")[-1]] 
                header += mime_type
                header += "\r\n\r\n"

                # read the requested file and copy it to response
                with open(address) as f:
                    page = ""
                    lines = f.readlines()
                    for line in lines:
                        page += line
            except FileNotFoundError:
                # for 404 page
                header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
                page = "<html>\
                        <body>\
                            <center>\
                            <h3>Error 404: Not Found</h3>\
                            </center>\
                        </body>\
                        </html>"
            
            except:
                # for 301
                # note that the browser will keep the record of redirecting
                # e.g. if browser sent a request about http://127.0.0.1:8080/deep and got redirected to  http://127.0.0.1:8080/deep/
                #      it is more likely the next time browser requests  http://127.0.0.1:8080/deep, the browser will change it to
                #      http://127.0.0.1:8080/deep/ automatically
                new_location = address + '/'
                new_location = new_location[5:]
                header = "HTTP/1.1 301 Moved Permanently\r\nContent-Type: text/html\r\nLocation: "+new_location+ "\r\n\r\n"
            
            final_response = header + page
            self.request.sendall(bytearray(final_response,'utf-8'))
        else:
            # for 405 page
            header = "HTTP/1.1 405 Method Not Allowed\r\n Content-Type: text/html\r\n\r\n"
            page = "<html>\
                          <body>\
                            <center>\
                             <h3>Error 405: Method Not Allowed</h3>\
                            </center>\
                          </body>\
                        </html>"

            final_response = header+page
            self.request.sendall(bytearray(final_response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 80

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
