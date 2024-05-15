import json
# from python_scripts.pinger import ping_all_machines
from is_network_up import get_targets, hit_target
from prometheus.prometheus_conf_writer import prometheus_conf_writer
import yaml
import os
import node_reservation
from grid5000 import Grid5000
import bartering_conf_builder
import subprocess
import socket
from is_network_up import get_targets, hit_target
from machine_test_starter import ping_machines_to_start
import time


## TODO GENERATE SWARM KEY !!!
with open("network_config_clusters.json","r") as f:
    config = json.load(f)

nodes_needed = int(config["IPFS_network"]["Nodes"])

test_length = config["TestLength"]

print(f"\nTest length : {test_length}")

username = config["Credentials"]

## CHECK CONFIG'S VALIDITY ##
if nodes_needed<2:
    print("\n\033[91mError : too few nodes ... you need at least two nodes in the network.\033[0m\n")
    exit(-1)

flag_clusters_to_build = False
try:
    clusters = config["IPFS_Clusters"]
    flag_clusters_to_build = True
except Exception as e:
    print("\nNo IPFSclusters detected in the configuration!\n")

flag_bartering = False
try:
    clusters = config["Bartering_network"]
    flag_bartering = True
except Exception as e:
    print("\nNo bartering nodes detected in the configuration!\n")

if flag_bartering:
    bartering_configs = config["Bartering_network"]["peers"]
    for key in bartering_configs.keys():
        try:
            # TODO check for all config validity
            data_copies = bartering_configs[key]['conf']["DataCopies"]
        except Exception as e:
            print("\nMissing DataCopies field in bartering config")
    total_nodes_bartering = sum([bartering_configs[key]["Nodes"] for key in bartering_configs.keys()])
    if total_nodes_bartering > nodes_needed:
        print("\n\033[91mError : you have defined more bartering nodes than there are nodes in the network. Please fix the configuration.\033[0m\n")
        exit(-1)


if flag_clusters_to_build:
    clusters_to_build = []
    nodes_in_clusters = 0
    for cluster in list(clusters.keys()):
        nodes_in_clusters += int(clusters[cluster]["Nodes"])
        clusters_to_build.append(clusters[cluster]["Nodes"])
    if nodes_in_clusters > nodes_needed:
        print("\n\033[91mError : you have defined more nodes in clusters than there are nodes in the network. Please fix the configuration.\033[0m\n")
        exit(-1)

print("\n\033[0;32mYour configuration passed the checks !\033[0m\n")


print(f"\nThe network needs {nodes_needed} nodes -- checking for availability ...\n")

conf_file = os.path.join(os.environ.get("HOME"), ".python-grid5000.yaml")

gk = Grid5000.from_yaml(conf_file)

# job, result = node_reservation.submit_job(gk, "lyon", "", nodes_needed, "debian11-min","0:03:30")

job = node_reservation.submit_job_and_only_job(gk, "lyon", "", nodes_needed, "debian11-min",test_length)

# TODO test if deployment OK (on result var), if not need to del job and abort test

# for node in result.keys():
#     print(f"node {node} : ",result[node]["state"])
#     if result[node]["state"]!='OK':
#         print("One of the nodes not OK - cannot continue job - will delete it")
#         os.system(f"oardel {job.uid}")
#         exit(-1)

with open("machines.txt","w") as f:
    for node in job.assigned_nodes:
        f.write(node)
        f.write('\n')

# print(job)
# print(job.uid) n           
# print(job.assigned_nodes)

os.system("kadeploy3 -f machines.txt debian11-min")

available_hosts = job.assigned_nodes

if len(available_hosts) < nodes_needed:
    print(f"\n\033[91mError : Not enough available nodes -- found {len(available_hosts)}, needed {nodes_needed} -- please change your configuration accordingly.\033[0m\n")
    exit(-1)
else:
    print(f"\n\033[0;32mFound {nodes_needed} available nodes, network can be built ! \033[0m\n")

#Elect bootstrap
#TODO add support for custom conf

bootstrap_node = available_hosts[0]
print(f"\nBootstrap chosen : {bootstrap_node}\n")


# Edit prometheus.yml
print("\nWriting Prometheus yaml file for data collection ...\n")
prometheus_conf_writer(available_hosts, 9101, "./prometheus/prometheus.yml")
print("\n\033[0;32mPrometheus file succesfully written ! \033[0m\n")

# Write ips.txt file for bartering bootstrap

print("\nWriting ips.txt file for bartering bootstrap ... \n")

def get_ip_from_domain(bootstrap_domain):
    out = subprocess.check_output(f"dig +short {bootstrap_domain}",shell=True)
    return out.decode()[:-1]

ips = [get_ip_from_domain(domain) for domain in available_hosts]

print("IPS : ", ips)

with open("./playbooks/bartering-protocol/ips.txt","w") as f:
    for ip in ips:
        f.write(ip+"\n")

print("\n ips.txt file for bartering bootstrap written in playbooks/bartering-protocol \n")

available_hosts.remove(bootstrap_node)


print("Building hosts.ini file ...")

with open("hosts/hosts.ini","w") as f:
    ip_address = socket.gethostbyname(bootstrap_node)
    f.write(f"[Bootstrap-node]\n{username}@{bootstrap_node} label=bootstrap label_ip={bootstrap_node} ip_address={ip_address}\n")
    f.write('\n')
    f.write(f"[IPFS-nodes]\n")
    n = 0
    for host in available_hosts:
        ip_address = socket.gethostbyname(host)
        f.write(f"{username}@{host} label=node{n} label_ip={host} ip_address={ip_address}\n")
        n +=1 
    f.write('\n')

print("\n\033[0;32mhosts.ini file successfully built!\033[0m\n")
    
available_hosts.append(bootstrap_node)

if flag_bartering:
    print("\nProvisioning nodes for Bartering ...")

    # Open model playbook 
    f = open("playbooks/playbook_backup.yml", "r") 
    existing_playbook = yaml.safe_load(f)
    f.close()

    with open("hosts/hosts.ini","a") as f:
        counter = 0
            
        # Get the IP address for the first host
        ip_address = socket.gethostbyname(available_hosts[0])
        
        
        # Write the host entry with IP address
        f.write(f"[BarteringBootstrap]\n")
        f.write(f"{username}@{available_hosts[0]} label=bartering-bootstrap label_ip={available_hosts[0]} ip_address={ip_address}\n")
    
        # Open model bootstrap playbook
        bootstrap_file = open("bartering_playbooks/model_bartering_bootstrap.yml", "r") 
        base_bootstrap = yaml.safe_load(bootstrap_file)
        bootstrap_file.close()

        # Modify whatever needs to be
        base_bootstrap[0]['hosts']=f"BarteringBootstrap"

        # Write into existing data
        existing_playbook.append(base_bootstrap[0])


       
        for key in bartering_configs.keys():
            f.write(f"[BarteringNodes{key}]\n")
            number_of_nodes = bartering_configs[key]["Nodes"]
            n = 0

            base_node_file = open("bartering_playbooks/model_bartering_nodes.yml", "r") 
            base_node = yaml.safe_load(base_node_file)
            base_node_file.close()

            base_node[0]['hosts']=f"BarteringNodes{key}"
            base_node[0]['vars']['group_name']=f"BarteringNodes{key}"

            existing_playbook.append(base_node[0])

            while n < number_of_nodes:
                ip_address = socket.gethostbyname(available_hosts[counter])
                f.write(f"{username}@{available_hosts[counter]} label=bartering-node{counter} label_ip={available_hosts[counter]} ip_address={ip_address}\n")
                n+=1
                counter +=1
    with open("playbooks/playbook.yml","w") as f:
        yaml.dump(existing_playbook,f)

    print("Building bartering configuration files ... ")

    output = bartering_conf_builder.extract_bartering_config("network_config_clusters.json")

    bartering_conf_builder.build_configs(output)

    print("Bartering network good to be deployed")




if flag_clusters_to_build:
    print("\nProvisioning nodes for IPFSClusters ...")

    with open("hosts/hosts.ini","a") as f:
        n = 0
        p = 1
        for cluster in clusters_to_build:
            for node in range(int(cluster)):
                if node == 0:
                    f.write(f"[IPFSCluster{p}_starter]\n")
                    f.write(f"{username}@{available_hosts[n]} label=node{n} label_ip={available_hosts[n]}\n")
                    f.write('\n')
                    if int(cluster)>1:
                        f.write(f"[IPFSCluster{p}]\n")
                    n+=1
                else:
                    f.write(f"{username}@{available_hosts[n]} label=node{n} label_ip={available_hosts[n]}\n")
                    n+=1
            f.write('\n')
                
            p+=1
    print("\n\033[0;32mClusters nodes initialized !\033[0m\n")

    print("\nModifying playbook accordingly ...")
    
    n = 0
    p = 1

    with open("playbooks/playbook_backup.yml", "r") as f:
        existing_data = yaml.safe_load(f)


    
    for cluster in clusters_to_build:
        with open("cluster_playbooks/model_cluster_starter.yml","r") as f1:
            starter_playbook_data = yaml.safe_load(f1)

        #print("DEBUG :",starter_playbook_data[0])
        starter_playbook_data[0]['hosts']=f"IPFSCluster{p}_starter"
        #print("DEBUG :",starter_playbook_data[0])

        with open("cluster_playbooks/model_cluster_nodes.yml","r") as f2:
            nodes_playbook_data=yaml.safe_load(f2)

        nodes_playbook_data[0]["hosts"]=f"IPFSCluster{p}"


        existing_data.append(starter_playbook_data[0])
        existing_data.append(nodes_playbook_data[0])
        
        p +=1
    
   
    with open("playbooks/playbook.yml","w") as f:
        yaml.dump(existing_data,f)

        

#TODO ADD SUPPORT FOR DIFFERENT CONFIG FOR EACH NODE

print("\nLaunching playbook ...")


os.system("ansible-playbook playbooks/playbook.yml -i hosts/hosts.ini")

print("\n Getting network status ... ")



time.sleep(10)

ping_machines_to_start(ips)

# Here, we consider network is up, and test is ready to start
# Next lines allow us to continuously diagnose network status during test
targets = get_targets()
while True:
    for target in targets:
        hit_target(target)
    time.sleep(10)
