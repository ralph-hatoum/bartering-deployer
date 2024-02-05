import os
import requests
import time
import datetime


site = "lyon"
cluster = "taurus"
timeout = 1 #timeout in minutes for the job to stay on 
walltime = "01:00"
number_of_nodes = 3
command = ""

"""curl -i https://api.grid5000.fr/stable/sites/grenoble/jobs?pretty -X POST -H'Content-Type: application/json' -d '{"resources": "nodes=2,walltime=02:00", "command": "while(true); do sleep 5; echo \"awake\"; done"}' """


def submit_job(gk, site, timeout, number_of_nodes, env, res_duration):
    site = gk.sites[site]

    job = site.jobs.create({"name": "bartering-deployment",
                        "command": "sleep 3600",
                        "types": ["deploy"],
                        "resources": f"nodes={number_of_nodes},walltime={res_duration}"})
    
    while job.state != "running":
        job.refresh()
        print("Waiting the job [%s] to be running" % job.uid)
        time.sleep(10)

    print("Assigned nodes : %s" % job.assigned_nodes)

    deployment = site.deployments.create({"nodes": job.assigned_nodes,
                                      "environment": env})

    while deployment.status != "terminated":
        deployment.refresh()
        print("Waiting for the deployment [%s] to be finished" % deployment.uid)
        time.sleep(10)

    print(deployment.result)
    print(f"Job id : {job.uid}")
    return job, deployment.result



def job_killer():
    return  





def reserve_nodes(site, cluster, timeout, number_of_nodes, command):
    api_job_url = f"https://api.grid5000.fr/stable/sites/{site}/jobs"

    payload = {
        "resources": f"nodes={number_of_nodes},walltime={walltime}",
        "command": command,
        "stdout": "api-test-stdout",
        "properties": f"cluster='{cluster}'",
        "name": "api-test"
    }

    job = requests.post(api_job_url, data=payload).json()
    print(job)
    job_id = job["uid"]

    current_time = datetime.datetime.now()

    while datetime.datetime.now() < current_time + datetime.timedelta(minutes=timeout):
        time.sleep(5)
        job_info = requests.get(api_job_url+f"/{job_id}").json()
        state = job_info['state']
        if state == "running":
            break

    if state!="running":
        print("Timed out")
        # TODO delete job from queue
        return 

    assigned_nodes = job_info["assigned_nodes"]

    return assigned_nodes






