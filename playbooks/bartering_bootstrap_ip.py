import subprocess
def get_ip_from_domain(bootstrap_domain):
    out = subprocess.check_output(f"dig +short {bootstrap_domain}",shell=True)
    return out.decode()[:-1]
import sys

args = sys.argv

if len(args) != 2:
    print("missing bootstrap domain name")
    exit(-1)

bootstrap_domain=args[1]

bootstrap_domain = bootstrap_domain.split("@")[1]


ip_address = get_ip_from_domain(bootstrap_domain)

print(ip_address)

with open("bartering-protocol/bootstrap_ip.txt","w") as f:
    f.write(ip_address)

