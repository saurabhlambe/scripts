#!/bin/bash

# This script will install and set up a Postgres-9.6 database for Ranger.

# Install Postgres-9.6
yum install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y
yum install postgresql96-contrib postgresql96-server -y

# Initialize postgres
/usr/pgsql-9.6/bin/postgresql96-setup initdb

# Append these lines to allow

# Define variables
db=ranger
user=rangeradmin

# Edit the config files
echo "local all postgres,ranger,rangerlogger trust
host all postgres,ranger,rangerlogger 0.0.0.0/0 trust
host all postgres,ranger,rangerlogger ::/0 trust" >> /var/lib/pgsql/9.6/data/pg_hba.conf
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /var/lib/pgsql/9.6/data/postgresql.conf
systemctl start postgresql-9.6

# Create database and assign role
su - postgres bash -c "psql -c \"CREATE DATABASE $db;\""
su - postgres bash -c "psql -c \"CREATE USER $user WITH PASSWORD 'bigdata';\""
su - postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $db TO $user;\""
su - postgres bash -c 'psql -c \\list'

# All you got to do is install Ranger using Ambari and specify the above details (database, username, password, hostname, etc)
