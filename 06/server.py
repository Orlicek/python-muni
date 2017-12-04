import os
import http.client
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl



class MineBaseHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip('/')
        if path:
            self.send_response(200, "OK")
            self.send_header('Content-type','text-html')
            self.end_headers()
            content = 'you asked for {0}'.format(path)
            self.wfile.write(bytes(content, encoding='UTF-8'))
            return
        else:
            try:
                with open("./main.html") as main_page_file:
                    self.send_response(200, "OK")
                    main_page = main_page_file.read()
                    self.send_header('Content-type','text-html')
                    self.end_headers()
                    self.wfile.write(bytes(main_page, encoding='UTF-8'))
                    return
            except IOError:
                self.send_error(404, 'Main page not found')

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def run():
  print('http server is starting...')

  server_address = ('127.0.0.1', 8000)
  httpd = HTTPServer(server_address, MineBaseHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()
