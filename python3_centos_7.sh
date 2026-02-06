#!/bin/bash
# Script to install Python3 on CentOS 7

# Preparing the System
yum -y install yum-utils
yum -y groupinstall development

# Installing and Setting Up Python 3
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python36u

# Check Python version
python3.6 -V

# Install pip
yum -y install python36u-pip
echo "Pip installed"
