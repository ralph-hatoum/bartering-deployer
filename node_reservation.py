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
    exit(-1)

assigned_nodes = job_info["assigned_nodes"]



