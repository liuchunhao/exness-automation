#!/bin/sh

# kill the listed processes below
# apps=("on_tick_server_exness" "on_trade_server_exness" "main" )

# for app in ${apps[@]}
# do
#    echo "[$app]"
#    ps -ef | grep "${app}" | grep -v grep | awk '{print $2}' | xargs kill -9
# done


[ -n "$(ps -ef | grep 'python' | grep -v grep)" ] && {
   ps -ef | grep "python" | grep -v grep | awk '{print $2}' | xargs kill -9
}

ps -ef | grep "python" | grep -v grep 

