

APP_HOME=$(dirname $(readlink -f $0))
cd $APP_HOME

# source ${APP_HOME}/.venv/bin/activate

pip3 install -r requirements.txt

python --version

sleep 1
python src/on_tick_server_binance.py &
python src/on_tick_server_exness.py &
python src/on_trade_server_exness.py &

