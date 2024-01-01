import os
import requests
from time import sleep

site = "lyon"
cluster = "taurus"


"""curl -i https://api.grid5000.fr/stable/sites/grenoble/jobs?pretty -X POST -H'Content-Type: application/json' -d '{"resources": "nodes=2,walltime=02:00", "command": "while(true); do sleep 5; echo \"awake\"; done"}' """

api_job_url = f"https://api.grid5000.fr/stable/sites/{site}/jobs"

payload = {
    "resources": "nodes=3,walltime=00:01",
    "command": "while(true); do sleep 5; echo \"awake\"; done",
    "stdout": "api-test-stdout",
    "properties": f"cluster='{cluster}'",
    "name": "api-test"
}

job = requests.post(api_job_url, data=payload).json()
print(job)
job_id = job["uid"]

sleep(60)
state = requests.get(api_job_url+f"/{job_id}").json()["state"]
print(state)