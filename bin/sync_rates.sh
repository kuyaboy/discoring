#!/bin/bash
set -o allexport
source .env
set +o allexport

CURRENCY="CHF"
FXRATES_API_URL="https://api.fxratesapi.com/latest?api_key=$FXRATES_API_TOKEN&base=$CURRENCY&places=2"
OUTPUT_FILE="src/config/exchange_rates.json"
STATUS_CODE=$(curl -s -o /dev/null -w "%{response_code}" "$FXRATES_API_URL")
ERROR_MESSAGE="ERROR: Could not sync exchange rate - $STATUS_CODE"
ENCODED_MESSAGE=$(echo "$ERROR_MESSAGE" | jq -sRr @uri)


if [ $STATUS_CODE -eq 200 ]
then
        curl -s "$FXRATES_API_URL" | jq '.' > "$OUTPUT_FILE"
        echo "Synced exchange rates for $CURRENCY"
else
        curl "${TELEGRAM_CHAT_URL}${ENCODED_MESSAGE}"
fi
