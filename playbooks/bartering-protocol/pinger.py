import subprocess
import os
import time
import socket

def get_own_ip():
    """Get the IP address of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

def ping_target(target):
    """Ping a single target IP and print the latency."""
    try:
        response = subprocess.run(
            ["ping", "-c", "1", target], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        if response.returncode == 0:
            latency = response.stdout.split('time=')[1].split(' ms')[0]
            print(f"Latency to {target}: {latency} ms")
        else:
            print(f"Failed to ping {target}")
    except Exception as e:
        print(f"Error pinging {target}: {e}")

def BuildPeersIPlist(file_path):
    """Read IP addresses from a text file."""
    with open(file_path, 'r') as file:
        peers = file.read().splitlines()
    return peers

def main():
    print("\nGetting network status ... ")
    own_ip = get_own_ip()
    peers = BuildPeersIPlist("./ips.txt")
    filtered_peers = [ip for ip in peers if ip != own_ip]
    
    print("\nMonitoring network status...")
    while True:
        for peer in filtered_peers:
            ping_target(peer)
        time.sleep(10)

if __name__ == "__main__":
    main()
