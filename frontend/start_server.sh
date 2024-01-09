#!/bin/bash


start_server()
{
        rm $dir/nohup_server.log

        nohup python3 server.py $@ > nohup_server.log 2>&1 &
        echo $! > save_pid_server.txt
        echo "server started and pid saved to file"
}

start_app()
{
        rm $dir/nohup_app.log

        nohup python3 app.py $@ > nohup_app.log 2>&1 &
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
