#!/bin/bash
# add additional dependencies required for your solution here.
# for example:
#pip3 install mysql-client
apt-get update && apt-get install -y \
sudo \
vim \
cron
crontab -l | { cat; echo "*/5 * * * * python3 /submissionscript/db_preupgrade.py /scripts/ dev mysql_container devopstt 123456"; } | crontab -
service cron start

sleep infinity