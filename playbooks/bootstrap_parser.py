import os
import sys
import subprocess

args = sys.argv

bootstrap_ip_address=args[1]


def get_ip_from_domain(bootstrap_domain):
    out = subprocess.check_output(f"dig +short {bootstrap_domain}",shell=True)
    return out.decode()[:-1]

bootstrap_ip_address = get_ip_from_domain(bootstrap_ip_address)

# ###   PARSE BOOTSTRAP ID ###
with open("id_secret/bootstrap_id.txt","r") as f:
    line = f.readlines()


peerId = line[0][20:-4]

ipfs_id_full = f"/ip4/{bootstrap_ip_address}/tcp/4001/ipfs/{peerId}"

os.system("rm -f bootstrap_id.txt")

with open("id_secret/bootstrap_id.txt", "w") as f:
    f.write(ipfs_id_full)

with open("id_secret/bootstrap_ip.txt", "w") as f:
    f.write(bootstrap_ip_address)


## PARSE CLUSTER SECRET ##

with open("id_secret/cluster_secret.txt","r") as f:
    line = f.readlines()

cluster_password = line[0][20:-5]

os.system("rm -f cluster_secret.txt")

with open("id_secret/cluster_secret.txt","w") as f:
    f.write(cluster_password)