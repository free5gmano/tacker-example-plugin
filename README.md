# tacker-example-plugin
> OS:Ubuntu 18.04

> OpenStack Version:Rocky

## Environment
1. OpenStack Cluster
> Install via Devstack

[https://docs.openstack.org/tacker/latest/install/devstack.html](https://docs.openstack.org/tacker/latest/install/devstack.html)

## Set up
1. OpenStack Create Network

| Network Name | Network Address |   Gateway IP  |
|--------------|-----------------|---------------|
|    public    |  192.168.2.0/24 | 192.168.2.254 |
|    net_mgmt  |  10.10.0.0/24   | 10.10.0.254   |

2. Update free5GC conf file

[/NSST/data](https://github.com/free5gmano/tacker-example-plugin/tree/master/NSST/data)

3. Update Tacker VIM information

[/allocate/params.py](/allocate/params.py)

4. Update NM Server IP

[/allocate/main.py](/allocate/main.py)

```python
def main():
    nfvo_plugin = NFVOPlugin('127.0.0.1',    # nm ip
                             OS_MA_NFVO_IP)  # os-ma-nfvo ip
    nfvo_plugin.allocate_nssi()
```
