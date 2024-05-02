import socket
import os
import time
import numpy as np

# Constants

PORT = 7000
DATA_DIRECTORY = "./data"
START_MESSAGE = "start"

# Assuming a Poisson distribution for file sizes (in KB) for simplicity

LAMBDA = 10

# File creation rate (files per second)

RATE = 1

# Create data directory if it doesn't exist

if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

# Start TCP server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

    server_socket.bind(('', PORT))
    server_socket.listen()
    print(f"Listening on port {PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            message = client_socket.recv(1024).decode('utf-8')
            message = message.strip()
            if message == START_MESSAGE:
                print("Start message received. Beginning data write.")
                break

    # Begin data generation

    while True:  # Replace with a suitable condition to stop the test
        file_size = np.random.poisson(LAMBDA) * 1024  # File size in bytes
        file_content = os.urandom(file_size)  # Generate random content
        file_path = os.path.join(DATA_DIRECTORY, f"{time.time()}.dat")      
        with open(file_path, 'wb') as file:
            file.write(file_content)     
        time.sleep(1/RATE)  # Adjust the rate of file creation

