import os
import time
import subprocess
import sys

def write_large_file(directory, filename, size_mb):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'wb') as f:
        f.write(b'\0' * (size_mb * 1024 * 1024))
args = sys.argv

if len(args) != 2:
    print("missing node  name")
    exit(-1)

node_name=args[1]


directory = './data'

# Modify the filename to include the node_name
filename = f'large_file_{node_name}.txt'
size_mb = 10

write_large_file(directory, filename, size_mb)
