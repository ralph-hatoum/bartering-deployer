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


def submit_job_and_only_job(gk, site, timeout, number_of_nodes, env, res_duration):
    site = gk.sites[site]

     # Modify the properties to include the specific clusters in Lyon
    clusters = ["gemini", "neowise", "nova", "orion", "pyxis", "sagittaire", "sirius", "taurus"]
    cluster_conditions = " OR ".join([f"cluster='{cluster}'" for cluster in clusters])
    properties = f"({cluster_conditions})"

     # Convert res_duration from "HH:MM:SS" to total seconds
    parts = res_duration.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError("Invalid time format. Please use 'HH:MM:SS'.")


    job = site.jobs.create({"name": "bartering-deployment",
                        "command": f"sleep {total_seconds}",  # Set sleep to the full duration of the walltime in seconds
                        "types": ["deploy"],
                        "resources": f"nodes={number_of_nodes},walltime={res_duration}",
                        "properties": properties    })
    
    while job.state != "running":
        job.refresh()
        print("Waiting the job [%s] to be running" % job.uid)
        time.sleep(10)

    print("Assigned nodes : %s" % job.assigned_nodes)

    return job
def submit_job_and_only_job_res(gk, site, number_of_nodes, env, res_duration, start_hour):
    # Current date and time
    current_time = datetime.datetime.now()

    # Parse hour and minute from start_hour
    start_dt = datetime.datetime.strptime(start_hour, "%H:%M")

    # Adjust start_dt to today's date
    start_dt = current_time.replace(hour=start_dt.hour, minute=start_dt.minute, second=0, microsecond=0)

    # If start time is in the past, adjust it to the next day
    if start_dt <= current_time:
        start_dt += datetime.timedelta(days=1)

    site_obj = gk.sites[site]

    # Modify the properties to include the specific clusters in Lyon
    clusters = ["gemini", "neowise", "nova", "orion", "pyxis", "sagittaire", "sirius", "taurus"]
    cluster_conditions = " OR ".join([f"cluster='{cluster}'" for cluster in clusters])
    properties = f"({cluster_conditions})"
    
     # Convert res_duration from "HH:MM:SS" to total seconds
    parts = res_duration.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError("Invalid time format. Please use 'HH:MM:SS'.")



    # Creating the job with specified walltime and start time
    job = site_obj.jobs.create({
        "name": "scheduled-deployment",
        "command": f"sleep {total_seconds}",  # Set sleep to the full duration of the walltime in seconds
        "types": ["deploy"],
        "resources": f"nodes={number_of_nodes},walltime={res_duration}",
        "properties": properties,
        "reservation": start_dt.strftime("%Y-%m-%d %H:%M:%S")
    })

    while job.state != "running":
        job.refresh()
        print(f"Waiting for the job [{job.uid}] to start running...")
        time.sleep(10)

    print(f"Job [{job.uid}] is running with nodes: {job.assigned_nodes}")
    return job


def submit_job(gk, site, timeout, number_of_nodes, env, res_duration):
    site = gk.sites[site]
    
    # Modify the properties to include the specific clusters in Lyon
    clusters = ["gemini", "neowise", "nova", "orion", "pyxis", "sagittaire", "sirius", "taurus"]
    cluster_conditions = " OR ".join([f"cluster='{cluster}'" for cluster in clusters])
    properties = f"({cluster_conditions})"
    
    # Convert res_duration from "HH:MM:SS" to total seconds
    parts = res_duration.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError("Invalid time format. Please use 'HH:MM:SS'.")



    job = site.jobs.create({"name": "bartering-deployment",
                        "command": f"sleep {total_seconds}",  # Set sleep to the full duration of the walltime in seconds,
                        "types": ["deploy"],
                        "resources": f"nodes={number_of_nodes},walltime={res_duration}",
                        "properties": properties})
    
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






