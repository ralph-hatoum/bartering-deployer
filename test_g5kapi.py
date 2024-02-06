import node_reservation
from grid5000 import Grid5000
import os
import time

site = "lyon"
cluster = "taurus"
timeout = 1 #timeout in minutes for the job to stay on 
walltime = "01:00"
number_of_nodes = 3
command = ""


def submit_job(gk, site, timeout, number_of_nodes, env, res_duration):
    site = gk.sites[site]

    job = site.jobs.create({"name": "bartering-deployment",
                        "command": "sleep 3600",
                        "types": ["deploy"],
                        "resources": f"nodes={number_of_nodes},walltime={res_duration}"})
    
    while job.state != "running":
        print(job.state)
        job.refresh()
        print("Waiting the job [%s] to be running" % job.uid)
        time.sleep(10)

    print("Assigned nodes : %s" % job.assigned_nodes)

    deployment = site.deployments.create({"nodes": job.assigned_nodes,
                                      "environment": env})

    while deployment.status != "terminated":
        print(deployment.status)
        deployment.refresh()
        print("Waiting for the deployment [%s] to be finished" % deployment.uid)
        time.sleep(10)

    print(deployment.result)
    print(f"Job id : {job.uid}")
    return job, deployment.result

conf_file = os.path.join(os.environ.get("HOME"), ".python-grid5000.yaml")

gk = Grid5000.from_yaml(conf_file)

job, result = submit_job(gk,site, "",3,"debian11-min","0:03:30")

print("result ",result)

print("job ",job)

nodes = []

for node in result.keys():
    print(result[node]["state"])
    if result[node]["state"]=='OK':
        nodes.append(node)
    else :
        print("One of the nodes not OK - cannot continue job - will delete it")
        os.system(f"oardel {job.uid}")
        exit(-1)
        break

print(nodes)