# Bartering deployer

Project to deploy my [bartering based IPFS overlay](https://github.com/ralph-hatoum/pr-bartering) on Grid5000 nodes.

Largely inspired by a previous [deployer](https://github.com/ralph-hatoum/PR2022-2024) I made to deplot IPFS and IPFSCluster on ssh-accessible nodes.

## Requirements and preliminary precisions
You'll need access to the Grid5000 network.
Once you have this, the recommended workflow is the following :

- Edit and configure the files of this repo on your machine
- Whenever you are ready to deploy, scp the folder to the Grid5000 frontend of whichever site you want to use
- Launch the project from the site frontend

Avoid editing files on the Grid5000 frontend ; it is impractical to do so in Vi or Nano, and using VSCode to edit files over SSH seems to overload the frontend and cause problems for **all** people connecting to the frontend (source: Grid5000 mailing list discussion).

## Deploy
In the inf_builder.py, you have to choose your test's durantion. Be careful that this needs to take into account the time to deploy. After that, all you need to do is edit the network_config_clusters.json file : 
```
{
    "Credentials":"root",
    "IPFS_network":
    {
        "Nodes": 4,
        "GCPeriod": "15m",
        "MaxStorage": "15kb"
        
    },
    "Bartering_network": 
    {
        "FailureModel": "weibull",
        "peers":
        {
            "1": 
            {
                "Nodes": 2,
                "conf": 
                {
                "TotalStorage": 150000,
                "NodeProfile": "peer",
                "BarteringInitialScore": 10.0,
                "BarteringFactorAcceptableRatio": 0.3,
                "BarteringRatioIncreaseRate": 0.1,
                "StoragerequestsScoreDecreaseRefusedStoReq": 0.8,
                "StoragetestingTimerTimeoutSec": 5,
                "StoragetestingTestingPeriod": 20,
                "StoragetestingFailedTestTimeoutDecrease": 0.5,
                "StoragetestingFailedTestWrongAnsDecrease": 0.7,
                "StoragetestingPassedTestIncrease":0.2
                }
            }, 
            "2": 
            {
                "Nodes": 2,
                "conf": 
                {
                "TotalStorage": 1500,
                "NodeProfile": "peer",
                "BarteringInitialScore": 10.0,
                "BarteringFactorAcceptableRatio": 0.312312,
                "BarteringRatioIncreaseRate": 0.12132,
                "StoragerequestsScoreDecreaseRefusedStoReq": 0.8,
                "StoragetestingTimerTimeoutSec": 5,
                "StoragetestingTestingPeriod": 2013,
                "StoragetestingFailedTestTimeoutDecrease": 0.5131,
                "StoragetestingFailedTestWrongAnsDecrease": 0.7,
                "StoragetestingPassedTestIncrease":0.2
                }
            }

        }
    }
}
```
Fields are fairly straightforward, but if you need more info on what to put, check out the [original deployer](https://github.com/ralph-hatoum/PR2022-2024)'s doc and the [bartering based IPFS overlay](https://github.com/ralph-hatoum/pr-bartering) repo for bartering node configurations.

Once you have your configuration and all your files have been copied to the G5K fronted via scp, run ./deploy.sh

The code was tested on the G5K Lyon frontend so as long as enough nodes are available, there should be no errors.


## Debugging
In case there is indeed an error, understand the deployer is a python script that :
- checks the configuration
- reserves and deploys G5K nodes on debian11-min by default
- writes ansible playbooks and hosts file
- launches the ansible playbook

This means the deployer can file during the python execution, or during the ansible playbook execution. If it fails in the former, it is likely that a module is missing, or that there was an issue in the parameters. Either way, debugging will happen in the inf_builder.py script. However, it it fails in the latter, the issue is likely that the commands that are by ansible on remote nodes are not going well, and the only way to debug this is to connect to a reserved and deployed node to run the command and see what happens. It is a painfully long process that you hopefully won't need to be doing as this has been tested on the same machine you will be running from.

## Contributing
It is important to note that any changes in the configuration of the bartering nodes in the [bartering based IPFS overlay](https://github.com/ralph-hatoum/pr-bartering) repo will result in a breaking change here. In this case, the bartering_conf_builder.py script will need to be updated to account for config changes, as well as change the base config in bartering_playbooks.

## Dashboard
The only way to be sure the network is running correctly is to have a grafana dashboard with information about ipfs being up on nodes and bartering being up on nodes.

On each node deployed, we will run a python script called node_exporter.py whose job is to start a http server listening on a defined port and provide a response with all needed metrics when a call to the /metrics endpoint happens. 

Then, on another machine, the one from which we'd like to see the dasboard, run prometheus whose job is to periodically hit the /metrics endpoint of all nodes to collect data. The inf_builder has code to write the prometheus config.

As of 15/02/24, the dashboard does not work yet, as I have not found a way to get a graphical interface on the frontend.

But if you hit < node address >:9101/metrics with curl, you should be able to see metrics
