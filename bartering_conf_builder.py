import json
import subprocess
import yaml


def extract_bartering_config(config_path):
    with open(config_path,"r") as f:
        config = json.load(f)


    bartering_conf = config["Bartering_network"]

    failure_model = bartering_conf["FailureModel"]

    output = []

    peers = bartering_conf["peers"]

    for key in peers.keys():
        host_type = f"BarteringNodes{key}"
        number_of_nodes = peers[key]["Nodes"]
        output.append([host_type, number_of_nodes, failure_model ,peers[key]["conf"]])

    # print(output)
    return output

# conf_list = extract_bartering_config("./network_config.json")

def check_if_different_and_change(key, value, conf):
    if conf[key] != value:
        conf[key] = value

def build_configs(config_list):
    with open("bartering_playbooks/base-config.yaml", "r") as f:
        conf = yaml.safe_load(f)
    # print(base_conf["FailureModel"])
    for node_type in config_list:
        subprocess.run(["mkdir",f"playbooks/bartering-protocol/{node_type[0]}"])
        check_if_different_and_change("FailureModel", node_type[2], conf)
        for key in node_type[3].keys():
            check_if_different_and_change(key, node_type[3][key], conf)
        with open(f"playbooks/bartering-protocol/{node_type[0]}/conf.yaml", "w") as conf_file:
            yaml.dump(conf, conf_file, default_flow_style=False)

# build_configs(conf_list)

# with open("network_config.json","r") as f:
#     config = json.load(f)
# bartering_configs = config["Bartering_network"]["peers"]
# total_nodes_bartering = sum([bartering_configs[key]["Nodes"] for key in bartering_configs.keys()])
# print(total_nodes_bartering)

def write_in_playbooks(config_list):
    return