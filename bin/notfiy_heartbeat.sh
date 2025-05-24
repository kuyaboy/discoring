#!/usr/bin/bash
set -o allexport
source .env
set +o allexport

TELEGRAM_API_TEST_URL=https://api.telegram.org/bot$TELEGRAM_API_TOKEN/getMe
STATUS_CODE=$(curl -s -o /dev/null -w "%{response_code}" "$TELEGRAM_API_TEST_URL")
HEARTBEAT_MESSAGE="Hello it's me - I'm still running :)"
ENCODED_HEARTBEAT_MESSAGE=$(echo "$HEARTBEAT_MESSAGE" | jq -sRr @uri)


if [ $STATUS_CODE -eq 200 ]
then
        curl "${TELEGRAM_CHAT_URL}${ENCODED_HEARTBEAT_MESSAGE}"
else
        echo "Something has gone wrong with sending the 'ENCODED_HEARTBEAT_MESSAGE'..."
fi
