from node_reservation import submit_job_and_only_job
import os
from grid5000 import Grid5000

conf_file = os.path.join(os.environ.get("HOME"), ".python-grid5000.yaml")

gk = Grid5000.from_yaml(conf_file)

job = submit_job_and_only_job(gk, "lyon","", 1, "debian11-min", "00:10:00")


with open("machines.txt","w") as f:
    for node in job.assigned_nodes:
        f.write(node)
        f.write('\n')

print(job)
print(job.uid)
print(job.assigned_nodes)

os.system("kadeploy3 -f machines.txt debian11-min")