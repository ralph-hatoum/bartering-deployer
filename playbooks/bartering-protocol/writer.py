import os
import time

def write_large_file(directory, filename, size_mb):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'wb') as f:
        f.write(b'\0' * (size_mb * 1024 * 1024))

directory = './data'
filename = 'large_file.txt'
size_mb = 10

time.sleep(600)

write_large_file(directory, filename, size_mb)