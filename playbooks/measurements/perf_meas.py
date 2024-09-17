import socket
import requests
import time
# import ipfsApi
import json
import os
import random

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 65434)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

PEERS = []

with open("./machines.txt", "r") as f:
    PEERS = f.readlines()

PEERS = list(map(lambda x : x[:-1], PEERS))

print('Waiting for a connection...')

def from_str_to_list(s):
    s = s.split(" ")
    output = []
    for element in s:
        if element != 'recursive\n':
            output.append(element)
    return output

START = True

while not START:
    # Wait for a connection
    connection, client_address = server_socket.accept()
    data = connection.recv(16)
    if data:
        message = data.decode('utf-8')
        if "GO" in message:
            print('Received "GO" message, starting collection')
            # Place the rest of the code here
            START = True
        else:
            connection.close()


# First, get list of locally pinned CIDs

response = requests.get('http://localhost:9101/metrics')
if response.status_code == 200:
    data = response.json()
    metrics_dict = dict(data)
else:
    print(f"Failed to retrieve metrics. Status code: {response.status_code}")

self_cids = from_str_to_list(metrics_dict['ipfs_pinned'])

# Get CIDS pinned at peers

peer_cids = []

cids_at_peers = {}

for peer in PEERS:
    print(peer)
    try:
        response = requests.get(f'http://{peer}:9101/metrics', timeout=10)
    except Exception as e:
        continue
    if response.status_code == 200:
        data = response.json()
        metrics_dict = dict(data)
    else:
        print(f"Failed to retrieve metrics. Status code: {response.status_code}")

    cids = from_str_to_list(metrics_dict['ipfs_pinned'])

    cids_at_peers[peer] = cids

    for cid in cids:
        peer_cids.append(cid)


#  Now, find CIDs not stored on self, but on peers

cids_to_grab = []

for cid in peer_cids:
    if cid not in self_cids:
        cids_to_grab.append(cid)

# Avoid duplicates

cids_to_grab = list(dict.fromkeys(cids_to_grab))
random.shuffle(cids_to_grab)

print("CIDS TO GRAB : ", cids_to_grab)

def grab_from_ipfs(cid, count, cids_grabbed):
    start_time = time.time()
    try:
        requests.post(f"http://127.0.0.1:5001/api/v0/get?stream-channels=true&archive=true&compress=true&encoding=json&arg={cid}", timeout=60)
        cids_grabbed.append(cid)
    except Exception as e:
        print(e)
    end_time = time.time()
    elapsed_time = end_time - start_time

    os.system(f"rm -f {cid}")

    return elapsed_time, count+1

def def_grab_from_ipfs(cid):
    start_time = time.time()
    try:
        requests.post(f"http://127.0.0.1:5001/api/v0/get?stream-channels=true&archive=true&compress=true&encoding=json&arg={cid}", timeout=60)
    except Exception as e:
        print(e)
    end_time = time.time()
    elapsed_time = end_time - start_time

    os.system(f"rm -f {cid}")

    return elapsed_time


data = {}
count = 0
cids_grabbed = []

for cid in cids_to_grab:
    print(cid)
    data[cid], count = grab_from_ipfs(cid, count, cids_grabbed)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)
    if count >= 10:
        break

with open('data.json', 'w') as json_file:
    json.dump(data, json_file)

data_2 = {}

for cid in cids_grabbed:
    print(cid)
    data_2[cid] = def_grab_from_ipfs(cid)
    with open('data-2.json', 'w') as json_file:
        json.dump(data_2, json_file)

with open('data-2.json', 'w') as json_file:
    json.dump(data_2, json_file)