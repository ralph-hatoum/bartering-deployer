from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import psutil
import sys

# Define the port number to listen on
PORT = 9100
if len(sys.argv)!=2:
    print("Needs folder as argument - exiting - error")
    exit(-1)

FOLDER = sys.argv(1)

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    #print(total_size)
    return total_size

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

# Create a custom request handler by subclassing BaseHTTPRequestHandler
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set the response status code
        self.send_response(200)

        # Set the response headers
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        endpoint = self.path[1:]

        if endpoint=="metrics":

            file_size_str = str(getFolderSize(FOLDER))
            current_timestamp = int(time.time() * 1000)

            ipfs_running = is_process_running("ipfs")

            # Set the response content
            response_text = f"ipfs_up {ipfs_running} {current_timestamp} \nipfs_blocks_size {file_size_str} {current_timestamp}"

            # Send the response content as bytes
            self.wfile.write(response_text.encode('utf-8'))

        return

# Create an HTTP server with the custom request handler
httpd = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
print(f"Server running on port {PORT}")

# Start the server
httpd.serve_forever()
