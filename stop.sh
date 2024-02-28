
# kill the listed processes below
apps = ("on_tick_server", "python3.6", "python3.7", "python3.8")
ps -ef | grep "python3" | grep -v grep | awk '{print $2}' | xargs kill -9