# IoT-miniproject-2-Coap-Server
This is a repository is part of a course work for course  Internet of Things - Universioty of Oulu.


# IoT-miniproject-2-Coap-Server

## Overview

### Introduction

**IoT-miniproject-2-Coap-Server** is the part of the project work assigned at the Internet of Things (521043S-3004) course at University of Oulu in 2023. The base for this CoAp server is taken from [here](https://github.com/matluuk/IoT-miniproject-1.git).

### Table of Contents

- [Video demonstration](#video-demonstration)
- [Create linux virtual machine](#create-linux-virtual-machine)
    - [Set up Google cloud VM](#set-up-google-cloud-vm)
    - [Create Virtual private cloud](#create-virtual-private-cloud)
    - [Firewall rules](#firewall-rules)
    - [Create VM instance](#create-vm-instance)
- [Set up CoAP server](#set-up-coap-server)
    - [Install all the dependencies and set up the python3 virtual environment.](#install-all-the-dependencies-and-set-up-the-python3-virtual-environment)
    - [Start CoAp server](#start-coap-server)
    - [LOGS](#logs)
    - [DATA](#data)
- [Code Structure](#code-structure)
- [Authors](#authors)

## Video demonstration
[Link to video demonstration](https://youtu.be/paAgqlTc-Gs)

## Create linux virtual machine

For CoAp server a linux virtual machine is needed. Any linux virtual machine should work, but we walk through how to set up Google Cloud virtual machine. Google cloud has a free trial with 300$ credits to use. The virtual machine needs a external IPV6 ip address for connection with the iot-lab node. 

Requirements for the virtual machine:
- runs linux, preferably Ubuntu 20.04
- has external IPV6 address for connecting with iot-lab nodes, as RIOT supports only ipv6
- CoAp port 8683 open
- ICMPv6 traffic allowed
- SSH connection to the VM

### Set up Google cloud VM

Google Cloud account is needed for using google Cloud services. At the time being, 300 credits can be obtained for use in 3 months time period for free. Below are a link to where a google cloud account can be created.

https://console.cloud.google.com/?hl=en&_ga=2.87814171.-2055644655.1699615458&_gac=1.116033140.1702051941.CjwKCAiAmsurBhBvEiwA6e-WPIQOg4lsX1QJevny4vxo9FBotFtCxOCFgTHR5MXrhSOSkf66HEamdRoCthsQAvD_BwE

### Create Virtual private cloud

Next step is to create vpc (virtual private cloud) for the VM. This is necessary to get the external ipv6 address for the VM. The VPC:s can be managed at following google cloud console site.

https://console.cloud.google.com/networking/networks?hl=en&_ga=2.16771894.-1464318792.1699625730&_gac=1.195093086.1701470264.CjwKCAiApaarBhB7EiwAYiMwqnFJQWu6iGIMccKLYWIfXNoxHQGC0UXqAEzLXMDN3NWpUHO9M_Fa9RoC834QAvD_BwE

VPC can be created by pressing the `CREATE VPC NETWORK` button on the top bar.

![CREATE VPC NETWORK](images/createVpcNetwork.png)

Below are all the setting I used to create the VPC.

<details><summary>VPC settings</summary>

![VPC settings 1](images/vpcsettings1.png)

![VPC settings 2](images/vpcsettings2.png)

Select all these firewall rules for both ipv4 and ipv6!

![VPC settings 3](images/vpcsettings3.png)

![VPC settings 4](images/vpcsettings4.png)

</details>

### Firewall rules

Firewall rules are a set of instructions that control how a firewall device handles incoming and outgoing traffic. They are access control mechanisms that enforce security in networks by blocking or allowing communication based on predetermined criteria. 

Firewall rules can be managed at Google Cloud firewall rules website: 

https://console.cloud.google.com/net-security/firewall-manager/firewall-policies

For the coap server, a firewall rule that allows udp traffic on CoAp port 8683 must be created.
This rule can be created by clicking the `CREATE FIREWALL RULE` button and using the following settings: 

![CREATE FIREWALL RULE](images/createFirewallRule.png)

<details><summary>Firewall rule: allow udp 8683</summary>

![Firewall rule CoAp 1](images/firewallCoap1.png)

![Firewall rule CoAp 2](images/firewallCoap2.png)

</details>

If you have followd according to this tutorial, you should have these firewall rules for the newly created VPC. Notice, that there are also some firewall rules for default VPC.

![Firewall rules](images/firewallrules.png)

If the firewall rules of your VPC are similar, you can continue.

### Create VM instance

The Virtual machine is used to deploy the Coap server. Google cloud VM:s can be managed from the Google Cloud console instances website.

https://console.cloud.google.com/compute/instances

Click the `CREATE INSTANCE` button. And change the settings mentioned on the dropdown below.

![Alt text](images/createinstance.png)

<details><summary>VM instance settings</summary>

Notice! It is important that the VM region is the same as the VPC subnet region.
For the machine type I have chosen the e2-small. This have been enough for the CoAp server.

![VM instance settings 1](images/VMinstance1.png)

The linux image should be changed to Ubuntu 20.04 under `Boot Disk`

![VM instance settings 2](images/VMinstance2.png)

Under Advanced options the Networking settings must be changed. 

1. Change the Network interface from default to the newly created VPC. 
2. The subnetwork should be automatically selected to the one that you created.
3. Select the `IP stack type` to be IPv4 and IPv6 (dual-stack)

![VM instance settings 3](images/VMinstance3.png)
</details>

Now everything should be properly set up and the VM instance can be created. The instance should dispaly the external ipv6 address.

![SSH to VM](images/VMinstance4.png)

The SSH connection to the VM instance can be made by clicking the SSH button under Connect. This creates new window with the ssh connection.

## Set up CoAP server

Connect to the linux VM, where you want the the CoAp server to be deployed.

### Install all the dependencies and set up the python3 virtual environment.

1. Clone the repository to your folder of choise:

    ```bash
    git clone https://github.com/matluuk/IoT-miniproject-1.git
    ```

2. move to the Coap server directory
    ```bash
    cd IoT-miniproject-1/Coap-Server/
    ```

3. update apt-get
    ```bash
    sudo apt-get update
    ```

4. Create python venv

    * install python3.8-venv
        ```bash
        sudo apt install python3.8-venv -y
        ```

    * Create the python venv 
    
        Notice - Use the start_server.sh script activates the venv automatically, so use exactly the same venv location and name

        ```bash
        python3 -m venv ./venv
        ```

    * Activate the python venv
        ```bash
        source ./venv/bin/activate
        ```

5. install aiocoap

    First all dependencies have to be installed:

    * install autoconf on linux 

        ```bash
        sudo apt-get install autoconf -y
        ```

    * install python-dev for 

        ```bash
        sudo apt-get install python-dev-is-python3 -y
        ```

    * install build-essential

        ```bash
        sudo apt-get install build-essential -y
        ```

    * Finally install aiocoap to the activated python venv

        ```bash
        pip3 install --upgrade "aiocoap[all]"
        ```

6. Install flask
    * install flask
        ```bash
        pip3 install flask
        ```
    * install flask-cors
        ```bash
        pip3 install flask-cors
        ```
### Start CoAp server

1. Check the external ipv6 address for your VM.

    * Install net-tools
        ```bash
        sudo apt-get install net-tools -y
        ```
    * Check the external ipv6 address
        ```bash
        ifconfig
        # output:
        ens4: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1460
                inet 10.0.0.5  netmask 255.255.255.255  broadcast 0.0.0.0
                inet6 fe80::4001:aff:fe00:5  prefixlen 64  scopeid 0x20<link>
                inet6 2600:1900:4150:368:0:3::  prefixlen 128  scopeid 0x0<global> # Take the ipv6 address from this line
                ether 42:01:0a:00:00:05  txqueuelen 1000  (Ethernet)
                RX packets 10765  bytes 114444072 (114.4 MB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 7960  bytes 938787 (938.7 KB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

        lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
                inet 127.0.0.1  netmask 255.0.0.0
                inet6 ::1  prefixlen 128  scopeid 0x10<host>
                loop  txqueuelen 1000  (Local Loopback)
                RX packets 216  bytes 22910 (22.9 KB)
                RX errors 0  dropped 0  overruns 0  frame 0
                TX packets 216  bytes 22910 (22.9 KB)
                TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        ```

2. Start the CoAp server using your external ipv6 address and port 8683
    ```bash
    sh start_server.sh ip=<external-ipv6-address-of-the-VM> port=8683
    ```

The `start_server.sh` uses nohup to start the server. Press `enter` to go back to console. 

Server are now running on the background and can be stopped using the `stop_server.sh` script.
```bash
sh stop_server.sh
```
### LOGS

The CoAp server saves logs of every session to `logs` folder. To take a look on the log created. 
1. Go to the `logs` folder:
    ```bash
    cd logs
    ```

2. The `tail` command can be used to show the logs in real time.
    ```bash
    tail -f ./<name-of-the-lates-log-file>.log
    ```
### DATA

The temperature data is stored in files under data folder. One file is made for each day, when temperature datais received. Notice that the data folder is created, when the first temperature vaule is received.

1. Go to the `data` folder:
    ```bash
    cd data
    ```
2. The temperature data can be shown using the `tail` command.
    ```bash
    tail -f ./<name-of-the-lates-data-file>.txt
    ```
    Or the latest file can be shown using this command:
    ```bash
    tail -f `ls -t | head -1`
    ```

## Unittests

### Coverage
    With following command the unittest coverage report can be created.
    ```bash
    pytest --cov=. --cov-report=html tests/
    ```

## Code Structure

The project has the following code structure:

```plaintext
.
├── server.py
├── start_server.sh
├── stop_server.sh
├── images
│   └── ...
└── README.md
```

## Authors

- **Matti Luukkonen** - [GitHub Profile](https://github.com/matluuk)
