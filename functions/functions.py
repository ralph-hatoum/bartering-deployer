import json
import os
import node_reservation
from grid5000 import Grid5000
import subprocess
import yaml
import bartering_conf_builder

def extract_params_from_config(config_path):
    """
    Extract all needed parameters from the json config file

    Args:
    - config_path (str) : path to json config file

    Returns:
    - int : nodes needed for the cluster
    - str : length of the test
    - str : username to use for ssh connections
    - bool : flag to know if IPFSCluster nodes were defined
    - bool : flag to know if bartering nodes were defined
    """
    # Open config file
    with open(".json","r") as f:
        config = json.load(f)

    nodes_needed = int(config["IPFS_network"]["Nodes"])

    test_length = config["TestLength"]

    username = config["Credentials"]

    flag_clusters_to_build = False

    try :
        clusters = config["IPFS_Clusters"]
        flag_clusters_to_build = True
    except:
        print("\nNo IPFSclusters detected in the configuration! In case you have defined clusters and they were not detected, you have probably made a mistake in the syntax and should refer to the readme.\n")

    flag_bartering = False

    try:
        bartering = config["Bartering_network"]
        flag_bartering = True
    except Exception as e:
        print("\nNo bartering nodes detected in the configuration! In case you have defined nodes and they were not detected, you have probably made a mistake in the syntax and should refer to the readme.\n")

    return nodes_needed, test_length, username, flag_clusters_to_build, flag_bartering

def check_configurations_validity(nodes_needed, flag_clusters_to_build, flag_bartering, config):
    """
    Check if the configuration is valid 
    Checks performed :
        - Is there more than 2 nodes defined ?
        - Is the number of nodes in IPFS Clusters equal or less than the number of nodes defined in total ?
        - Is the number of bartering nodes equal or less than the number of nodes defined in total ?

    Args:
    - nodes_needed (int) : number of nodes defined in the configuration
    - flag_clusters_to_build (bool) : true if IPFSClusters to build, false otherwise
    - flag_bartering (bool) :  true if bartering nodes defined, false otherwise
    - config (dict) : config file in dict array

    Returns:
    - bool : true if checks passed, false otherwise
    """
    if nodes_needed<2:
        print("\n\033[91mError : too few nodes ... you need at least two nodes in the network.\033[0m\n")
        return False

    if flag_bartering:
        bartering_configs = config["Bartering_network"]["peers"]
        total_nodes_bartering = sum([bartering_configs[key]["Nodes"] for key in bartering_configs.keys()])
        if total_nodes_bartering > nodes_needed:
            print("\n\033[91mError : you have defined more bartering nodes than there are nodes in the network. Please fix the configuration.\033[0m\n")
            return False

    if flag_clusters_to_build:
        clusters = config["IPFS_Clusters"]
        clusters_to_build = []
        nodes_in_clusters = 0
        for cluster in list(clusters.keys()):
            nodes_in_clusters += int(clusters[cluster]["Nodes"])
            clusters_to_build.append(clusters[cluster]["Nodes"])
        if nodes_in_clusters > nodes_needed:
            print("\n\033[91mError : you have defined more nodes in clusters than there are nodes in the network. Please fix the configuration.\033[0m\n")
            return False
        
    return True

def exit_if_true(boolean):
    """
    Exit process if boolean is true

    Args:
    - boolean (bool)
    """
    if boolean:
        exit(-1)

def build_hosts_file(username, bootstrap_node, available_hosts):
    """
    Build hosts.ini file for Ansible

    Args:
    - username (str) : username to use for ssh connection
    - bootstrap_node (str) : bootstrap node for the ipfs network
    - available_hosts (str list) : list of hosts available for deployment
    """
    with open("hosts/hosts.ini","w") as f:
        f.write(f"[Bootstrap-node]\n{username}@{bootstrap_node} label=bootstrap label_ip={bootstrap_node}\n")
    f.write('\n')
    f.write(f"[IPFS-nodes]\n")
    n = 0
    for host in available_hosts:
        f.write(f"{username}@{host} label=node{n} label_ip={host}\n")
        n +=1 
    f.write('\n')

def g5k_reservation(site, number_of_nodes, env, test_length):
    """
    Create Grid5000 job 

    Args:
    - site (str) : Grid5000 site
    - number_of_nodes (int) : number of nodes in the reservation
    - env (str) : os distribution nodes will run on
    - test_length (str) : length of the test (also the job reservation duration)

    Returns:
    - dict : job output from Grid5000 reservation
    """
    conf_file = os.path.join(os.environ.get("HOME"), ".python-grid5000.yaml")

    gk = Grid5000.from_yaml(conf_file)

    job = node_reservation.submit_job_and_only_job(gk, site, "", number_of_nodes, env,test_length)

    return job

def write_nodenames(job):
    """
    Write names of nodes in text file for the kadeploy command

    Args:
    - job (dict) : job output from Grid5000 reservation
    """
    with open("machines.txt","w") as f:
        for node in job.assigned_nodes:
            f.write(node)
            f.write('\n')

def deploy_nodes_root_access():
    """
    Call kadeploy to reboot nodes on new OS to get root access
    """
    os.system("kadeploy3 -f machines.txt debian11-min")

def get_ip_from_domain(bootstrap_domain):
    """
    Get IP from domain name
    (basically, the g5k API for job reservation will return reserved node names as <node-name>.<site>.grid5000.fr ; we need the corresponding IP 
    to open TCP sockets in the bartering code)

    Args:
    - bootstrap_domain (str) : node domain name

    Returns:
    - str : IP address of the node
    """
    out = subprocess.check_output(f"dig +short {bootstrap_domain}",shell=True)
    return out.decode()[:-1]

def write_ips_file(available_hosts):
    """
    Write IP addresses in a text file 
    (the bootstrap needs to know the IPs of the bartering nodes, so we write them all in a file to give to the bootstrap)

    Args:
    - available_hosts (list of str) : list of the available hosts
    """
    ips = [get_ip_from_domain(domain) for domain in available_hosts]
    print("IPS : ", ips)
    with open("./playbooks/bartering-protocol/ips.txt","w") as f:
        for ip in ips:
            f.write(ip+"\n")

def add_bootstrap_nodes_to_hosts_and_playbooks(existing_playbook, username, available_hosts, bartering_configs):
    """
    Add everything needed for bartering nodes in the hosts.ini and playbook.yml files

    Args:
    - existing_playbook (dict) : opened existing playbook file
    - username (str) : username for ssh connecton
    - available_hosts (list of str) : names of hosts to deploy
    - bartering_configs (list of dicts) : extracted bartering configs from config
    """
    with open("hosts/hosts.ini","a") as f:
        counter = 0
        f.write(f"[BarteringBootstrap]\n{username}@{available_hosts[0]} label=bartering-bootstrap label_ip={available_hosts[0]}\n")

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
                f.write(f"{username}@{available_hosts[counter]} label=bartering-node{counter} label_ip={available_hosts[counter]}\n")
                n+=1
                counter +=1
        with open("playbooks/playbook.yml","w") as f:
            yaml.dump(existing_playbook,f)

        print("Building bartering configuration files ... ")

        output = bartering_conf_builder.extract_bartering_config("network_config_clusters.json")

        bartering_conf_builder.build_configs(output)

        print("Bartering network good to be deployed")