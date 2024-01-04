import os
import subprocess

available_hosts =[]


def pinger(host):
    flag = False
    ping_command = ["ping", "-c", "3",host]
    try: 
        output = subprocess.check_output(ping_command, stderr=subprocess.STDOUT)
        flag = True
    except subprocess.CalledProcessError as e:
        flag = False
        output = e.output
    #print(output)
    if flag:
        print(f"Host {host} : \033[0;32mAvailable!\033[0m")
    else:
        print(f"Host {host} : \033[91mUnavailable\033[0m")
    return flag


def ping_all_machines(n):
    with open("hosts/ip_@.txt",'r') as f:
        hosts = f.readlines()
    hosts = list(map(lambda x:x[:-1] if (x[-1]=='\n') else x,hosts))
    available_hosts = []
    for host in hosts:
        if pinger(host):
            available_hosts.append(host)
        if len(available_hosts) == n:
            break
    
    return available_hosts

    