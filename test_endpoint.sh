#!/bin/sh

test_endpoint() {
    response=$(curl -s -X 'POST' \
        'http://127.0.0.1:8000/predict' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "{
        \"sep_len\": $1,
        \"sep_wdt\": $2,
        \"pet_len\": $3,
        \"pet_wdt\": $4
        }" | jq '.ypred')

    [ "$response" -eq "$5" ] || echo "Test failed: response ($response) does not equal $5"
}

test_endpoint 5.1 3.5 1.4 0.2 0
test_endpoint 7.0 3.2 4.7 1.4 1
test_endpoint 6.3 3.3 6.0 2.5 2
test_endpoint 4.9 3.0 1.4 0.2 0
