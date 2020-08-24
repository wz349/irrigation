#!/bin/bash

JWT_TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiJhZmY4NzI0MC1hOTBmLTExZWEtYTUyYS02MTQyM2U3NTY2Y2IiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiYWZkYjc0NjAtYTkwZi0xMWVhLWE1MmEtNjE0MjNlNzU2NmNiIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNTk0MDYwMzYwLCJleHAiOjE1OTQwNjkzNjB9.wX3EbM2Z7r82-es6Hf8ju8DmoZP39ZKJDPwuS1DxCgAFtDYdjYlSdBlIIf1zHn5vcHvRm_Nm5t5TDzcffTwZYQ"
THINGSBOARD_URL="192.168.1.117:8080"
DEVICEID="8c1fef30-a912-11ea-96db-afc62de9cadc"
KEYS="temperature"
ENDTS="1594061287000"
OUTFILE="tb-data.json"
curl -X GET --header 'Accept: */*' --header "Content-Type:application/json" --header "X-Authorization: Bearer ${JWT_TOKEN}" "${THINGSBOARD_URL}/api/plugins/telemetry/DEVICE/${DEVICEID}/values/timeseries?keys=${KEYS}&startTs=978307200000&endTs=${ENDTS}&agg=NONE&limit=100000000" -o $OUTFILE
