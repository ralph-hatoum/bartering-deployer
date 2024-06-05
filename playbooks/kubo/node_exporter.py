from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import psutil
import sys
import json

# Define the port number to listen on
PORT = 9101

args = sys.argv

node_name = args[1]

ROOT = f"IPFS_nodes/{node_name}/kubo"
# FOLDER = f"IPFS_nodes/{node_name}/kubo/.ipfs"
FOLDER = "./data"

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
            return 1
    return 0

def list_pinned_cid():
    # List pin cid and retrieve them to show in grafana
    os.system(f"ipfs pin ls > ./output.txt")
    with open("output.txt",'r') as f:
        lines = f.readlines()
    output = " ".join(lines)
    return output
    
def build_json_response(ipfs_running, ipfs_clus_running, pinned, bartering_bootstrap_running, bartering_running, timestamp,file_size_str):
    return {"timestamp": timestamp, "ipfs_up": ipfs_running, "ipfs_blocks_size": file_size_str,"ipfs_clus_up":ipfs_clus_running, "bartering_bootstrap_running":bartering_bootstrap_running, "ipfs_pinned": pinned, "bartering_running":bartering_running}

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
            ipfs_clus_running = is_process_running("ipfs-cluster-service")
            pinned = list_pinned_cid()
            bartering_bootstrap_running = is_process_running("bootstrap")

            bartering_running = is_process_running("bartering")

            # Set the response content
            # response_text = f"ipfs_up {ipfs_running} {current_timestamp} \nipfs_blocks_size {file_size_str} {current_timestamp} \nipfs_clus_up {ipfs_clus_running} {current_timestamp} \nbartering_bootstrap_running {bartering_bootstrap_running} {current_timestamp} \nipfs_pinned {pinned} {current_timestamp} \nbartering_running {bartering_running} {current_timestamp}\n" 
            reponse_json = {"timestamp": current_timestamp, "ipfs_up": ipfs_running, "ipfs_blocks_size": file_size_str,"ipfs_clus_up":ipfs_clus_running, "bartering_bootstrap_running":bartering_bootstrap_running, "ipfs_pinned": pinned, "bartering_running":bartering_running}
            # """\nipfs_pinned {pinned} {current_timestamp}"""
            encoded = json.dumps(reponse_json).encode('utf-8')
            # Send the response content as bytes
            self.wfile.write(encoded)

        return

# Create an HTTP server with the custom request handler
httpd = HTTPServer(("", PORT), SimpleHTTPRequestHandler)
print(f"Server running on port {PORT}")

# Start the server
httpd.serve_forever()
