import socket

def build_machines_list_with_port(machines):
    output = []
    for machine in machines:
        output.append((machine, 7000))
    return output

def ping_machines_to_start(machines):
    peers = build_machines_list_with_port(machines)
    for ip, port in peers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                sock.sendall("start".encode('utf-8'))
                print(f"Sent start message to {ip}:{port}")
        except ConnectionRefusedError as e:
            print(f"Connection to {ip}:{port} refused: {e}")
        except socket.error as e:
            print(f"Socket error occurred with {ip}:{port}: {e}")
