export DEBIAN_FRONTEND=noninteractive

echo "Set Time Zone"
timedatectl set-timezone America/Los_Angeles

echo "Add deadsnakes PPA"
add-apt-repository -y ppa:deadsnakes/ppa

echo "Install base Ubuntu dependencies"
apt-get update
apt-get install -y apt-transport-https \
                   ca-certificates \
                   curl \
                   software-properties-common

echo "Add Ubuntu Dependencies"
apt-get install -y build-essential \
                   git \
                   git-flow \
                   python3-dev \
                   python3-pip \
                   python3.5 \
                   python3.7 \
                   python3.8 \
                   tig \
                   tree

echo "Installing python dependencies"

/usr/bin/python3 -m pip install --upgrade -r /vagrant/requirements_dev.txt
