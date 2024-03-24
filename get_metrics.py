from is_network_up import *
import datetime
import json
import time
import sys
import signal


TARGETS = get_targets()

current_time = datetime.datetime.now()

COLLECTION_TIME = current_time.strftime("%H:%M:%S")

OUTPUT_FILE = f"collected_data/test_{COLLECTION_TIME}.json"

RETRIEVAL_PERIOD=2 # in seconds

test_data = """ipfs_up 1 1711185189389
ipfs_blocks_size 46011967 1711185189389
ipfs_clus_up 0 1711185189389
bartering_bootstrap_running 0 1711185189389
ipfs_pinned QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn recursive
 1711185189389
bartering_running 1 1711185189389"""

def initiate_file():
    with open(OUTPUT_FILE, "w+") as file:
        file.write("{}")

def format_metric(value, timestamp):
    return {"Value": value, "Timestamp": timestamp}

def write_in_json_file(file_name, metric_name, to_append):
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    if metric_name in data.keys():
        data[metric_name].append(to_append)
    else:
        data[metric_name] = [to_append]
    with open(file_name, "w") as json_file:
        json.dump(data, json_file)
    
def write_in_output(response):
    response = response.split('\n')
    for metric in response:
        metric = metric.split(' ')
        try:
            metric_name = metric[0]
            metric_value = metric[1]
            timestamp = metric[2]
            to_append = format_metric(metric_value, timestamp)
            write_in_json_file(OUTPUT_FILE, metric_name, to_append)
        except:
            print("Invalid metric")

def signal_handler(sig, frame):
    global stopped
    print("Gracefully shutting down")
    stopped = True

if __name__=="__main__":
    initiate_file()
    stopped = False
    signal.signal(signal.SIGINT, signal_handler)
    while not stopped:
        for target in targets:
            response = hit_target_return_answer(target)
            write_in_output(test_data)
        time.sleep(2)
