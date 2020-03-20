  
#!/bin/sh
sudo apt-get update
sudo apt-get -y install mongodb wget git
sudo systemctl start mongodb

wget -q https://storage.googleapis.com/golang/getgo/installer_linux
chmod +x installer_linux
./installer_linux
source ~/.bash_profile
rm -f installer_linux

echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
echo 'export PATH=$PATH:$GOPATH/bin:$GOROOT/bin' >> ~/.bashrc
echo 'export GO111MODULE=off' >> ~/.bashrc
source ~/.bashrc
go get -u -v "github.com/gorilla/mux"
go get -u -v "golang.org/x/net/http2"
go get -u -v "golang.org/x/sys/unix"

ls -al /dev/net/tun

sudo sh -c "cat << EOF > /etc/systemd/network/99-free5gc.netdev
[NetDev]
Name=uptun
Kind=tun
EOF"

sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd

sysctl -n net.ipv6.conf.uptun.disable_ipv6
sudo sh -c "echo 'net.ipv6.conf.uptun.disable_ipv6=0' > /etc/sysctl.d/30-free5gc.conf"
sudo sysctl -p /etc/sysctl.d/30-free5gc.conf

sudo sh -c "cat << EOF > /etc/systemd/network/99-free5gc.network
[Match]
Name=uptun
[Network]
Address=45.45.0.1/16
Address=cafe::1/64
EOF"

sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd

sudo apt-get -y install net-tools

ifconfig uptun

sudo apt-get -y install autoconf libtool gcc pkg-config git flex bison libsctp-dev libgnutls28-dev libgcrypt-dev libssl-dev libidn11-dev libmongoc-dev libbson-dev libyaml-dev

git clone https://bitbucket.org/nctu_5g/free5gc-stage-1.git
cd free5gc-stage-1
autoreconf -iv
./configure --prefix=`pwd`/install
make -j `nproc`
make install

sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'
