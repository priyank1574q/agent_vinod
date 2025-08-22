#!/bin/bash
# Script to export AWS credentials from JSON file as environment variables

JSON_FILE="/home/ec2-user/aws_credentials_proper.json"

if [ -f "$JSON_FILE" ]; then
    export AWS_ACCESS_KEY_ID=$(python3 -c "import json; print(json.load(open('$JSON_FILE'))['access_key'])")
    export AWS_SECRET_ACCESS_KEY=$(python3 -c "import json; print(json.load(open('$JSON_FILE'))['secret_access_key'])")
    export AWS_DEFAULT_REGION=$(python3 -c "import json; print(json.load(open('$JSON_FILE'))['region'])")
    
    echo "AWS credentials exported as environment variables:"
    echo "AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID:0:10}..."
    echo "AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY:0:10}..."
    echo "AWS_DEFAULT_REGION: $AWS_DEFAULT_REGION"
else
    echo "Credentials file not found: $JSON_FILE"
fi
