import os
import requests
from time import sleep

# user = input(f"Grid'5000 username (default is {os.getlogin()}): ") or os.getlogin()
# password = input("Grid'5000 password (leave blank on frontends): ")
# g5k_auth = (user, password) if password else None

site_id = "lyon"
cluster = "taurus"

api_job_url = f"https://api.grid5000.fr/stable/sites/{site_id}/jobs"

api_deployment_url = f"https://api.grid5000.fr/stable/sites/{site_id}/deployments"

payload = {
    "resources": "nodes=1,walltime=00:10:00",
    "command": "sleep 600",
    "stdout": "api-test-stdout",
    "types": ["deploy"],
    "name": "api-test"
}

job = requests.post(api_job_url, data=payload).json()
job_id = job["uid"]

print(f"Job submitted ({job_id})")

state = ""

while state != "running":
    sleep(10)
    state = requests.get(api_job_url+f"/{job_id}").json()["state"]
    print(f"Waiting the job {job_id} to be running, currently {state}")

nodes = requests.get(api_job_url+f"/{job_id}").json()["assigned_nodes"]

payload = {"nodes":nodes, "environment":"debian11-min"}

deployment = requests.post(api_deployment_url, data=payload).json()

deployment_id = deployment["uid"]

deployment_state = ""

while deployment_state != "terminated":
    sleep(10)
    deployment_state = requests.get(api_deployment_url+f"/{deployment_id}").json()["state"]
    print(f"Waiting the deployment {deployment_id} to be terminated, currently {deployment_state}")

print(nodes)




