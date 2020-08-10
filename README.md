# tacker-example-plugin
> OS:Ubuntu 18.04

> OpenStack Version:Rocky

## Environment
### OpenStack Cluster
> Install via Devstack

[https://docs.openstack.org/tacker/latest/install/devstack.html](https://docs.openstack.org/tacker/latest/install/devstack.html)

1. Configure the second interface as the provider interface(controller node & compute node)
```shell
$ vim /etc/network/interfaces
# The provider network interface
auto ens3
iface ens3 inet manual
up ip link set dev $IFACE up
down ip link set dev $IFACE down
```
2. Update library(controller node & compute node)
```shell
$ sudo apt-get update
```
3. Add Stack User(controller node & compute node)
```shell
$ sudo useradd -s /bin/bash -d /opt/stack -m stack
$ echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
$ sudo su - stack
```
4. Download DevStack(controller node & compute node)
```shell
$ git clone https://git.openstack.org/openstack-dev/devstack -b stable/rocky
$ cd devstack
```
### Install controller node
1. Create a local.conf
> Update:HOST_IP,FLAT_INTERFACE,PUBLIC_INTERFACE

```shell
[[local|localrc]]
enable_plugin heat https://git.openstack.org/openstack/heat stable/rocky
enable_plugin tacker https://git.openstack.org/openstack/tacker stable/rocky
enable_plugin networking-sfc https://opendev.org/openstack/networking-sfc stable/rocky
enable_plugin barbican https://opendev.org/openstack/barbican stable/rocky
enable_plugin mistral https://opendev.org/openstack/mistral stable/rocky
enable_plugin aodh https://opendev.org/openstack/aodh stable/rocky

HOST_IP=CONTROLLER-IP
SERVICE_HOST=$HOST_IP
GIT_BASE=https://github.com
DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ADMIN_PASSWORD=password
MYSQL_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
SERVICE_TOKEN=$ADMIN_PASSWORD

enable_service n-novnc
enable_service n-cauth
disable_service tempest

NEUTRON_CREATE_INITIAL_NETWORKS=False
DOWNLOAD_DEFAULT_IMAGES=False

Q_PLUGIN=ml2
Q_AGENT=openvswitch

disable_service etcd3

MULTI_HOST=1

FLAT_INTERFACE=ens3
PUBLIC_INTERFACE=eno1
```
2. Start the install
```shell
$ ./stack.sh
```
### Install compute node
1. Create a local.conf
> Update:HOST_IP,SERVICE_HOST,PUBLIC_INTERFACE,FLAT_INTERFACE
```shell
[[local|localrc]]
SERVICE_HOST=CONTROLLER-IP
GIT_BASE=https://github.com
DATABASE_TYPE=mysql
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
KEYSTONE_AUTH_HOST=$SERVICE_HOST
KEYSTONE_SERVICE_HOST=$SERVICE_HOST
LOGFILE=/opt/stack/logs/stack.sh.log
ADMIN_PASSWORD=password
DATABASE_PASSWORD=password
RABBIT_PASSWORD=password
SERVICE_PASSWORD=password

PIP_UPGRADE=Flase

disable_service etcd3

# Neutron options
NEUTRON_CREATE_INITIAL_NETWORKS=False
MULTI_HOST=1

#---------------compute node common section
ENABLED_SERVICES=n-cpu,q-agt,n-api-meta,placement-client,n-novnc
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://$SERVICE_HOST:6080/vnc_auto.html"


#---------------compute node special section
HOST_IP=COMPUTE-IP
PUBLIC_INTERFACE=eno1
FLAT_INTERFACE=ens3
VNCSERVER_PROXYCLIENT_ADDRESS=$HOST_IP
VNCSERVER_LISTEN=$HOST_IP
```
2. Start the install
```shell
$ ./stack.sh
```
### Discover compute hosts
```shell
$ /opt/stack/devstack/tools/discover_hosts.sh
```
### Upload the image to the Image service
> Controller node
```shell
$ vim admin-openrc
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_AUTH_URL=http://CONTROLLER-IP/identity
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

$ . admin-openrc

# Ubuntu 16.04
$ wget http://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.img

$ openstack image create "ubuntu"   --file xenial-server-cloudimg-amd64-disk1.img   --disk-format qcow2 --container-format bare   --public
```
### Register VIM
> Update:CONTROLLER-IP,PROJECT-NAME
```shell
$ vim vim_config.yaml
auth_url: 'http://CONTROLLER-IP/identity'
username: 'admin'
password: 'password'
project_name: 'PROJECT-NAME'
project_domain_name: 'Default'
user_domain_name: 'Default'
cert_verify: 'False'

$ openstack vim register --config-file vim_config.yaml --description 'free5gc vim' --is-default free5gc
```
### Login OpenStack Cluster
OpenStack Dashboard:http://CONTROLLER-IP

username:admin

password:password

### Create free5gc image
1. Create Flavors

2. Create Neutron Network

3. Create Key Pairs

4. Create Security Groups

5. Launch Instance base on Ubuntu

6. ssh into instance

7. execation bash install free5gc
> file:[install.sh](https://github.com/free5gmano/tacker-example-plugin/blob/master/install.sh)

```shell
$ chmod +x ./install.sh
$ ./install.sh
```

8. Create a snapshot of the instance
> Controller node
```shell
$ vim admin-openrc
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_AUTH_URL=http://CONTROLLER-IP/identity
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2

$ . admin-openrc

$ nova list
+--------------------------------------+---------+--------+------------+-------------+-----------------------------------+
| ID                                   | Name    | Status | Task State | Power State | Networks                          |
+--------------------------------------+---------+--------+------------+-------------+-----------------------------------+
| 405cfb3f-b78c-4aca-9900-69f99b9e68d7 | free5gc | ACTIVE | -          | Running     | net_mgmt=10.10.0.18, 192.168.2.73 |
+--------------------------------------+---------+--------+------------+-------------+-----------------------------------+

$ nova stop free5gc
Request to stop server free5gc has been accepted.

$ nova list
+--------------------------------------+---------+---------+------------+-------------+---------------------+
| ID                                   | Name    | Status  | Task State | Power State | Networks            |
+--------------------------------------+---------+---------+------------+-------------+---------------------+
| 405cfb3f-b78c-4aca-9900-69f99b9e68d7 | free5gc | SHUTOFF | -          | Shutdown    | net_mgmt=10.10.0.18 |
+--------------------------------------+---------+---------+------------+-------------+---------------------+

$ nova image-create --poll free5gc free5gc_v1
Server snapshotting... 100% complete
Finished

$ openstack image list
+--------------------------------------+--------------------------+--------+
| ID                                   | Name                     | Status |
+--------------------------------------+--------------------------+--------+
| b497c57e-79f9-42d7-949d-756269eb8139 | free5gc_v1               | active |
| d065c1d9-abc2-4133-95f9-a30a12b1667b | ubuntu                   | active |
+--------------------------------------+--------------------------+--------+
```

9. Download the snapshot as an image
```shell
$ openstack image list
+--------------------------------------+--------------------------+--------+
| ID                                   | Name                     | Status |
+--------------------------------------+--------------------------+--------+
| b497c57e-79f9-42d7-949d-756269eb8139 | free5gc_v1               | active |
| d065c1d9-abc2-4133-95f9-a30a12b1667b | ubuntu                   | active |
+--------------------------------------+--------------------------+--------+

$ glance image-download --file free5gc_v1.raw b497c57e-79f9-42d7-949d-756269eb8139
```

10. Import the snapshot to the new environment
```shell
$ openstack image create "free5gc"   --file free5gc_v1.raw   --disk-format qcow2 --container-format bare   --public
```

## Set up
1. OpenStack Create Network

| Network Name | Network Address |   Gateway IP  |
|--------------|-----------------|---------------|
|    public    |  192.168.2.0/24 | 192.168.2.254 |
|    net_mgmt  |  10.10.0.0/24   | 10.10.0.254   |

2. Update free5GC conf file

> file:[/NSST/data](https://github.com/free5gmano/tacker-example-plugin/tree/master/NSST/data)

3. Update Tacker VIM information

> file:[/allocate/params.py](/allocate/params.py)

4. Update NM Server IP

> file:[/allocate/main.py](/allocate/main.py)

