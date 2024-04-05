#!/bin/sh


ps -ef | grep ngrok | grep -v grep | awk '{print $2}' | xargs kill -9

APP_HOME=$(dirname $(readlink -f $0))
echo $APP_HOME
cd $APP_HOME

nohup ngrok start --all --config ./ngrok.yml --log stdout & # | tee -a ngrok.log &
