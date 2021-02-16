# Script to set up cloud machines

sudo apt update

sudo apt install -y nano git screen unzip zip

# Install nordvpn
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh) -y

# Docker installation and use as sudo

sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install -y docker-ce
# sudo systemctl status docker

sudo usermod -aG docker ${USER}
su - ${USER}
id -nG

# Install last version of docker compose

sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose