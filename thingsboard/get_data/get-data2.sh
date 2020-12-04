#!/bin/bash
JWT_TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJ1c2VySWQiOiIwYzJlZmMwMC1jYTU4LTExZWEtOGEyMi04ZmZmMTc3YTQ1MjgiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMGJjMDViYjAtY2E1OC0xMWVhLThhMjItOGZmZjE3N2E0NTI4IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNTk4NDgwODc4LCJleHAiOjE1OTg0ODk4Nzh9.d9uQ79cqxrURum9FXFkbfuBh1-aVnJcgC0iCamhct9Ut6qqrg1DBmFWsXm2jJt8BCX-vFihSENGw_m0Ap_uZWw"
THINGSBOARD_URL="3.19.237.92:8080"
DEVICEID="b8780e70-ca58-11ea-8b49-d1b807b5b7ac"
KEYS="temperature3"
ENDTS="1598481057000" 
OUTFILE="tb-${KEYS}-data.json"
curl -X GET --header 'Accept: */*' --header "Content-Type:application/json" --header "X-Authorization: Bearer ${JWT_TOKEN}" "${THINGSBOARD_URL}/api/plugins/telemetry/DEVICE/${DEVICEID}/values/timeseries?keys=${KEYS}&startTs=978307200000&endTs=${ENDTS}&agg=NONE&limit=100000000" -o $OUTFILE
