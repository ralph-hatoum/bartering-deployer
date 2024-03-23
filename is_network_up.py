import yaml
import requests

def get_targets():
    with open("./prometheus/prometheus.yml") as file:
        data = yaml.safe_load(file)

    targets = data["scrape_configs"][1]["static_configs"][0]['targets']
    return targets

def hit_target(target):
    url = f"http://{target}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        format_and_print(data, target)    
    else:
        print("Request unsuccessful, node exporter probably not running")

test_data = """ipfs_up 1 1711185189389
ipfs_blocks_size 46011967 1711185189389
ipfs_clus_up 0 1711185189389
bartering_bootstrap_running 0 1711185189389
ipfs_pinned QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn recursive
 1711185189389
bartering_running 1 1711185189389"""

def format_and_print(data, target):
    data = data.split('\n')
    states = []
    for i in [0,3,-1]:
        data_split = data[i].split(' ')
        if data_split[1]=='1':
            states.append("\033[92mup\033[0m")
        else:
            states.append("\033[91mdown\033[0m")
    print(f""" 
    On node {target}
    IPFS is {states[0]}
    Bartering bootstrap is {states[1]}
    Bartering is {states[2]}
""")

if __name__=="__main__":
    targets = get_targets()
    for target in targets:
        hit_target(target)