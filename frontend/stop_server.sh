if kill -9 `cat save_pid_server.txt`; then
	rm save_pid_server.txt
	echo "server stopped"
fi

if kill -9 `cat save_pid_app.txt`; then
	rm save_pid_app.txt
	echo "app stopped"
fi
