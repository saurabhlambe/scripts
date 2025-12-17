#!/bin/bash

# This script will install and set up a Postgres-10 database for Ranger.

# Install Postgres-10
yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y
yum install postgresql10-contrib postgresql10-server -y

# Initialize postgres
/usr/pgsql-10/bin/postgresql96-setup initdb

# Define variables
# Replace db and user according you your needs
db=test
user=testadmin

# Edit the config files
echo "local all postgres,$user,rangerlogger trust
host all postgres,$user,rangerlogger 0.0.0.0/0 trust
host all postgres,$user,rangerlogger ::/0 trust" >> /var/lib/pgsql/10/data/pg_hba.conf
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /var/lib/pgsql/10/data/postgresql.conf
systemctl start postgresql-10
systemctl enable postgresql-10

# Create database and assign role
su - postgres bash -c "psql -c \"CREATE DATABASE $db;\""
su - postgres bash -c "psql -c \"CREATE USER $user WITH PASSWORD 'testpasswd';\""
su - postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $db TO $user;\""
su - postgres bash -c 'psql -c \\list'
echos "Postgres-10 installation and setup is complete"