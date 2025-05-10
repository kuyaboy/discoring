#!/bin/bash

echo "Starting Xvfb..."
su seluser -c "Xvfb :99 -ac 2>/dev/null &"

sleep 3
if pgrep -x "Xvfb" > /dev/null; then
    echo "Xvfb started successfully."
else
    echo "Xvfb failed to start. Exiting."
    exit 1
fi

# start cronjob as root
echo "Starting cronjob"
service cron start

echo "Running sync_wantlist.py..."

su seluser -c "/opt/venv/bin/python /app/bin/sync_wantlist.py"
if [ $? -ne 0 ]; then
    echo "sync_wantlist.py failed. Exiting."
    exit 1
fi

echo "Starting Discoring script..."
su seluser -c "/opt/venv/bin/python /app/src/main.py"
