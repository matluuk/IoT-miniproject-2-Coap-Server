#!/bin/bash

app_ip="127.0.0.1"
app_port="5000"

CoAp_server_ip="127.0.0.1"
CoAp_server_port="5683"

http_server_ip="127.0.0.1"
http_server_port="8000"

start_server()
{
        rm $dir/nohup_server.log

        nohup python3 server.py --ip=$http_server_ip --port=$http_server_port > nohup_server.log 2>&1 &
        echo $! > save_pid_server.txt
        echo "server started and pid saved to file"
}

start_app()
{
        rm $dir/nohup_app.log

        nohup python3 app.py --ip=$app_ip --port=$app_port --server_ip=$CoAp_server_ip --server_port=$CoAp_server_port > nohup_app.log 2>&1 &
        echo $! > save_pid_app.txt
        echo "App started and pid saved to file"
}

dir="$(pwd)"
. $dir/../venv/bin/activate

if [ -e save_pid_app.txt ]
then
	if kill -0 `cat save_pid_server.txt`; then
		echo "App is already running!"
	else
		start_app
	fi
else
        start_app
fi

if [ -e save_pid_server.txt ]
then
        if kill -0 `cat save_pid_server.txt`; then
                echo "Server is already running!"
        else
           start_server
        fi
else
        start_server
fi
