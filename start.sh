#!/bin/sh

APP_HOME=$(dirname $(readlink -f $0))
cd $APP_HOME

python --version

# virtualenv .venv

[ -e ${APP_HOME}/.venv/bin/activate ]     && source .venv/bin/activate 
[ -e ${APP_HOME}/.venv/Scripts/activate ] && source .venv/Scripts/activate 

python --version

echo $?

pip3 install -r requirements.txt

sleep 1

# python src/on_tick_server_binance.py &
nohup python src/on_tick_server_exness.py &
nohup python src/on_trade_server_exness.py &
nohup python src/main.py &

sleep 5

ps -ef | grep python | grep -v grep 
ps -ef | grep python | grep -v grep | grep on_tick_server_binance | awk '{print $2}'
ps -ef | grep python | grep -v grep | grep on_tick_server_exness  | awk '{print $2}'
ps -ef | grep python | grep -v grep | grep on_trade_server_exness | awk '{print $2}'
ps -ef | grep python | grep -v grep | grep main | awk '{print $2}'


netstat -na | grep TCP | grep LIST | egrep "5300|8765|18765"
