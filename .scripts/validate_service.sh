#!/usr/bin/env bash

echo "Waiting for 15 seconds before checking health.."
sleep 15

status_code=$(curl --write-out %{http_code} --silent --output /dev/null http://localhost:80/health)
if [[ "${status_code}" -ne 200 ]]; then
  echo "Application is not healthy - ${status_code}"
  exit 1
else
  echo "Application is responding with ${status_code}"
  exit 0
fi
