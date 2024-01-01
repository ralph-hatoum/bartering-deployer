import os
import sys

args = sys.argv

bootstrap_ip_address=args[1]


# ###   PARSE BOOTSTRAP ID ###
with open("id_secret/bootstrap_id.txt","r") as f:
    line = f.readlines()


peerId = line[0][20:-4]

ipfs_id_full = f"/ip4/{bootstrap_ip_address}/tcp/4001/ipfs/{peerId}"

os.system("rm -f bootstrap_id.txt")

with open("id_secret/bootstrap_id.txt", "w") as f:
    f.write(ipfs_id_full)

## PARSE CLUSTER SECRET ##

with open("id_secret/cluster_secret.txt","r") as f:
    line = f.readlines()

cluster_password = line[0][20:-5]

os.system("rm -f cluster_secret.txt")

with open("id_secret/cluster_secret.txt","w") as f:
    f.write(cluster_password)