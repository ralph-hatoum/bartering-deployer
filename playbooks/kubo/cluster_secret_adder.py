import json
import sys
from this import d

args = sys.argv

secret = args[1]
file_path = args[2]

with open(file_path,"r") as f:
    data = json.load(f)


data["cluster"]["secret"]=secret

with open(file_path,"w") as f:
    json.dump(data,f)

