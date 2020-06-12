<h1> <center> Demo Setup </center></h1>

## About the demo
AWS Lightsail has been used inorder to  create VMs.
Setup contains
- 3 instances of Amazon-Linux VMs
- 1 Amazon-Linux VM with Django installed. This is only so that python3 cones pre-installed in it.

## What happens in the demo?

The 3 VMs send their Utilisation files (util.txt) to another VM in which the allocator server is running. The server once it recieves the server adds the VM onto its list of VMs. Once it recieves 3 VMs it executes the following
- Independent Task2Vm and Dependent Task2VM for the files `network.py`, `compute.py`, `memory.py`
- Two examples on Dependent Task2VM

The scheduling queue is then shown for the 3 VMs.

## Server Setup
The server `server.py` is to be setup in the master VM. 
```
python3 server.py
```
Dependencies:
- `Flask` module
- `vm_allocator.py` module (custom made module. Given in code)
- `analyzer.py` module (custom made module. Given in code)



## Command to send util file from VM

The util files can either be taken from the ones given in code or new ones can be generated through the `utilisation.sh` bash script
```
chmod +x utilisation.sh
./utilsation.sh
```

The non-master VMs, VMs that are not running the allocator algorithm, send their utilisation file via a POST request 
```
curl -i -X POST http://<master_ip_address>:5000/util --data-binary "@util_file.txt"
```

## How to reproduce this demo

- Instantiate 4 VMs as mentioned above
- In the master VM get the necessary files by cloning into the repo
	```
	git clone https://github.com/shreyasseshadri/Major-Project.git
	```
- In the other 3 VMs either get the util files, either by generating by `utilsation.sh` or get the ones in the repo by `wget` command for each VM.
	```
	wget https://raw.githubusercontent.com/shreyasseshadri/Major-Project/master/util0.txt

	```
- Send the files from the 3 VMs to master through curl command as mentioned above.