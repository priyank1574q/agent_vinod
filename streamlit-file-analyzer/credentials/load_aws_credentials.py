#!/usr/bin/env python3
"""
Script to load AWS credentials from JSON file and set them as environment variables
or use them with boto3 clients.
"""

import json
import os
import boto3
from botocore.exceptions import ClientError

def load_credentials_from_json(json_file_path):
    """Load AWS credentials from JSON file."""
    try:
        with open(json_file_path, 'r') as f:
            creds = json.load(f)
        return creds
    except FileNotFoundError:
        print(f"Credentials file not found: {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in credentials file: {json_file_path}")
        return None

def set_environment_variables(credentials):
    """Set AWS credentials as environment variables."""
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['secret_access_key']
    print("AWS credentials set as environment variables")

def create_boto3_session(credentials):
    """Create a boto3 session with the loaded credentials."""
    session = boto3.Session(
        aws_access_key_id=credentials['access_key'],
        aws_secret_access_key=credentials['secret_access_key'],
        region_name='us-east-1'  # Set your preferred region
    )
    return session

def test_credentials(session):
    """Test the credentials by making a simple AWS API call."""
    try:
        sts_client = session.client('sts')
        response = sts_client.get_caller_identity()
        print(f"Credentials are valid. Account ID: {response['Account']}")
        print(f"User ARN: {response['Arn']}")
        return True
    except ClientError as e:
        print(f"Credentials test failed: {e}")
        return False

if __name__ == "__main__":
    # Load credentials from JSON file
    creds = load_credentials_from_json('/home/ec2-user/aws_cred.json')
    
    if creds:
        # Option 1: Set as environment variables
        set_environment_variables(creds)
        
        # Option 2: Create boto3 session
        session = create_boto3_session(creds)
        
        # Test the credentials
        if test_credentials(session):
            print("Ready to use AWS services!")
            
            # Example: List S3 buckets
            try:
                s3_client = session.client('s3')
                response = s3_client.list_buckets()
                print(f"Found {len(response['Buckets'])} S3 buckets")
                for bucket in response['Buckets']:
                    print(f"  - {bucket['Name']}")
            except ClientError as e:
                print(f"Error listing S3 buckets: {e}")
