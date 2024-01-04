#!/bin/bash
if [ -e save_pid.txt ]
then
	echo "Server is already running!"
else
	dir="$(pwd)"
	. $dir/../venv/bin/activate
	rm $dir/nohup.log

	nohup python3 server.py $@ > nohup.log 2>&1 &
	echo $! > save_pid.txt
fi
