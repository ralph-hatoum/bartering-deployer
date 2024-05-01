import socket

# To ping machines to start the test once deployment is done

def build_machines_list_with_port(machines):
    output = []
    for machine in machines:
        output.append((machine, 7000))
    return output

def ping_machines_to_start(machines):
    peers = build_machines_list_with_port(machines)
    # Send start message to each peer
    for ip, port in peers:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall("start".encode('utf-8'))
            print(f"Sent start message to {ip}:{port}")
