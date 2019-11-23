import http.server
import socketserver
import os
import sys



PORT = int(sys.argv[1])
# PATH = sys.argv[2]
PATH = "app"

web_dir = os.path.join(os.path.dirname(__file__), PATH )
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()