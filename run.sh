#!/bin/bash

python3 start_app.py &
sleep 5
python3 create_admin.py

while :; do
	sleep 300
done
