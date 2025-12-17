#!/bin/bash

echo # blank line
echo "This script installs Docker on CentOS"
echo # blank line

echo "Remove previous docker versions if they exist"
sudo yum remove docker \
	docker-client \
	docker-client-latest \
	docker-common \
	docker-latest \
	docker-latest-logrotate \
	docker-logrotate \
	docker-engine
echo # blank line

echo "Set up Docker repo"
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
echo # blank line

echo "Install Docker"
sudo yum install docker-ce docker-ce-cli containerd.io -y
echo # blank line

echo "Starting Docker"
sudo systemctl start docker
sudo systemctl enable docker
echo # blank line
echo # another blanmk line
echos "Docker installation completed"