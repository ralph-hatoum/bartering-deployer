from is_network_up import *
import datetime
import json
import time
import sys
import signal


# TARGETS = get_targets()

TARGETS=get_targets()

current_time = datetime.datetime.now()

COLLECTION_TIME = current_time.strftime("%H:%M:%S")

OUTPUT_FILE = f"collected_data/test_{COLLECTION_TIME}.json"

RETRIEVAL_PERIOD=2 # in seconds

test_data = """ipfs_up 1 1717619978175
ipfs_blocks_size 403456 1717619978175
ipfs_clus_up 0 1717619978175
bartering_bootstrap_running 1 1717619978175
ipfs_pinned QmTgDWLkLJToLbYX1vQwT21TUi8ypH56NnAv1fHqrTsTT3 recursive
 QmVWe1cZEjyd7hJwvujnoLvskGpPVhsv5WPQZX77XFswu2 recursive
 QmaagCWGdXcRQHzmuWHnfBC29jXzJaYrUu5fPtwKUBNVTN recursive
 QmbYH7R7QrechpJ2ey8QcNWt1GDmwAGE9T8NAUdHHK6nxt recursive
 Qmd6rx4Bjevu1QJQCCW3iZywebxPt3N6YWe1xiLjaFYiJ4 recursive
 Qmdsegw7XaTHQqm4agCPbVWbWs3Urogh1rhBMpgbRoAiHM recursive
 QmPzPAEgTnStQFxpCuDEGDp1KQLeMsfvyXYFtepntNMpmm recursive
 QmRrnxhxchJqJvYHFmP9DqkAoMXHsXasCQtmYeorMe5Cpo recursive
 QmWDHKpPXLQPVuRNftrqP8iYwagpCmDcXhpUQsrNxoDBo1 recursive
 QmX3ULSqKJqoNvVJRdCfEbK3BR1wiR3AucGbsNNLbJ6KFJ recursive
 QmNjtAbw9MtVjC7MgcW3AhuYj9Rgn7zP3yM65J6LyHhifv recursive
 QmPxwPSmRa8aK8napxrz4ZMJhVCtS9vAuqdSjvFB93s5Ve recursive
 QmSXnrKkxtUWAT1YAhMLfiUxhE9FnFa1jb4k5kQcFhnFXK recursive
 QmSgdj4pF4nZi7CWR8jgWTpWY1z4bNBPD5cy4RqNwBC9qj recursive
 QmTmJXnavr6qfAD3GsDQGL2tjE21p42fMAo7BcwjjYqJrR recursive
 QmV4QnZNP1ykRwgcZEotkLh39db7gA6GYtxL9SKtAGM7Te recursive
 QmVEFiBJP4sXsumteL43XuLSg3wth6JWfYvHkFxvkx76Za recursive
 QmXPNGYx3So13P6k3a5nqUw275hFL6VLZBZRLhfrqKqqru recursive
 Qmb5JdSbFnz4pebYVXrvtQdsCwrKm14zppBdgAx7sGZrXu recursive
 QmbAShiXtDkRBiiteLFUSQjuF6noGcm3SaWLKwTuEVbrRv recursive
 QmUNLLsPACCz1vLxQVkXqqLX5R1X345qqfHbsf67hvA3Nn recursive
 QmUNVUrVJgQVxd22NNrASQZVkKCZp9sRrCKxfUgpoSFyjz recursive
 QmX9Tv2Wfj26FGLayXfTFbGUGX4ts1wA9oceLfpYi6USWK recursive
 Qma3e84XMrh6vCth6Ehrex36GYWoBbaBsYNX87w31BSKfU recursive
 QmQhZoFH5E7tKS2P8hV2GX1Vkb1imk8ETBQoiJ27nAgkHh recursive
 QmTyN2oyXHbJduJndetJvFM5iMUTBPtmRS4JvRx6D89X2G recursive
 QmUc8bzR4kS4rv3aFCZsKV8gx92ycLGVj3yCAYGm5xcnFV recursive
 QmXHmzy6BUWFUUi76PWTWNyQz9hkS1zJPA8UEAKWNnqfDb recursive
 QmeHLfnMEteF8bo56Ko8zxAcnQGELf4m3gYZEq6TXPcZnh recursive
 QmeSW6daCipcqDYHBJrNDVECiTGM8tzHp5oBydT7iL6oET recursive
 QmV7QMC8zaivot9MyQZkrtpXPBEm19369PYSrsw7X1xno4 recursive
 QmVEKoVNJCEdSzobpBKmxsqY8NFbGmaWjPiEvJPRzg9ew4 recursive
 QmPWhf2RYy9tZimPYnay6bxjBim5guEu147jvJF22BTSRY recursive
 QmRKhfy3fLJufrwnd4xRKG3RGrKhDdYXVpKCSCuzWJNLaE recursive
 QmYaS5aJU6vA3QEtRnzADMHYjerbaqwDHTEgQxmYX3Z8rR recursive
 QmYy1bMb5Vjc7GKkyFHejQbFYgHW275iPsLQis7PShy8yf recursive
 QmeUX6UHVstKRErGF7hKwh9DAD9xMKStiSfJwddaGVpnhE recursive
 QmPm8GE8EA9Pyh5GtDgpWVjnMYZ92GbFVLf1W3TKPHHjRT recursive
 QmWoVqaJpKDmCh8gyjnuDdAgUkAvYi2xVVAdBAp8yWJ5fa recursive
 QmYkamsMKa787jmsu9e7rAJNqMQtvj8umhVp28kJ7bp2WB recursive
 QmZWa1xya5qh2CFKDC5KVi63gFiLtuRkdxmPSoPx4tKgrT recursive
 QmZhY9Q8bn6819gotKqow19yNsHMkdyxAawMvDvaFBwYDh recursive
 QmenVTtGh2L8N9v11rf2byWkYUfbk765hkyhWZXa8M1GsT recursive
 1717619978175
bartering_running 1 1717619978175"""

def initiate_file():
    with open(OUTPUT_FILE, "w+") as file:
        file.write("{}")
    with open(OUTPUT_FILE, "r") as file:
        data = json.load(file)
    for target in TARGETS:
        data[target]={}
    with open(OUTPUT_FILE, "w") as file:
        json.dump(data, file)

def format_metric(value, timestamp):
    return {"Value": value, "Timestamp": timestamp}

def write_in_json_file(file_name, metric_name, to_append, target):
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    if metric_name in data[target].keys():
        data[target][metric_name].append(to_append)
    else:
        data[target][metric_name] = [to_append]
    with open(file_name, "w") as json_file:
        json.dump(data, json_file)
    
def write_in_output(response, target):
    for metric in response:
        if metric == "timestamp":
            pass
        try:
            metric_name = metric
            metric_value = response[metric]
            timestamp = response["timestamp"]
            to_append = format_metric(metric_value, timestamp)
            write_in_json_file(OUTPUT_FILE, metric_name, to_append, target)
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
        for target in TARGETS:
            response = hit_target_return_answer(target)
            response_dic = json.loads(response)
            write_in_output(response_dic, target)
            print("Gathered data for host ",target)
        time.sleep(2)
