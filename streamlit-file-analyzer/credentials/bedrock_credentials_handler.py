#!/usr/bin/env python3
"""
Bedrock Credentials Handler
Handles loading and using credentials from bedrock.json file for AWS Bedrock access.
"""

import json
import os
import base64
import boto3
from botocore.exceptions import ClientError
from urllib.parse import parse_qs, urlparse
import re

class BedrockCredentialsHandler:
    def __init__(self, bedrock_json_path='/home/ec2-user/bedrock.json'):
        self.bedrock_json_path = bedrock_json_path
        self.credentials = None
        self.session = None
        
    def load_bedrock_credentials(self):
        """Load and parse credentials from bedrock.json file."""
        try:
            with open(self.bedrock_json_path, 'r') as f:
                content = f.read().strip()
            
            # The content appears to be base64 encoded
            if content.startswith('{') and content.endswith('}'):
                # Already JSON format
                creds_data = json.loads(content)
            else:
                # Try to decode base64
                try:
                    decoded_content = base64.b64decode(content).decode('utf-8')
                    if decoded_content.startswith('http'):
                        # This is a pre-signed URL, extract credentials from it
                        creds_data = self._extract_credentials_from_url(decoded_content)
                    else:
                        creds_data = json.loads(decoded_content)
                except Exception as e:
                    print(f"Error decoding bedrock.json: {e}")
                    # Try to parse as direct API key or token
                    creds_data = {"api_key": content}
            
            self.credentials = creds_data
            return creds_data
            
        except FileNotFoundError:
            print(f"Bedrock credentials file not found: {self.bedrock_json_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in bedrock credentials file: {e}")
            return None
        except Exception as e:
            print(f"Error loading bedrock credentials: {e}")
            return None
    
    def _extract_credentials_from_url(self, url):
        """Extract AWS credentials from a pre-signed URL."""
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            # Extract credentials from URL parameters
            credentials = {}
            
            if 'X-Amz-Credential' in query_params:
                credential_string = query_params['X-Amz-Credential'][0]
                # Format: ACCESS_KEY/date/region/service/aws4_request
                access_key = credential_string.split('/')[0]
                credentials['aws_access_key_id'] = access_key
            
            if 'X-Amz-Security-Token' in query_params:
                credentials['aws_session_token'] = query_params['X-Amz-Security-Token'][0]
            
            # Note: Secret key cannot be extracted from pre-signed URL
            # This URL is meant to be used directly for API calls
            credentials['presigned_url'] = url
            
            return credentials
            
        except Exception as e:
            print(f"Error extracting credentials from URL: {e}")
            return {"presigned_url": url}
    
    def create_bedrock_client(self, region='us-east-1'):
        """Create a Bedrock client using the loaded credentials."""
        if not self.credentials:
            self.load_bedrock_credentials()
        
        if not self.credentials:
            raise ValueError("No credentials available")
        
        try:
            # If we have AWS credentials
            if 'aws_access_key_id' in self.credentials:
                if 'aws_session_token' in self.credentials:
                    # Temporary credentials with session token
                    client = boto3.client(
                        'bedrock-runtime',
                        region_name=region,
                        aws_access_key_id=self.credentials['aws_access_key_id'],
                        aws_secret_access_key=self.credentials.get('aws_secret_access_key', ''),
                        aws_session_token=self.credentials['aws_session_token']
                    )
                else:
                    # Regular AWS credentials
                    client = boto3.client(
                        'bedrock-runtime',
                        region_name=region,
                        aws_access_key_id=self.credentials['aws_access_key_id'],
                        aws_secret_access_key=self.credentials['aws_secret_access_key']
                    )
            else:
                # Fall back to default credentials (environment, IAM role, etc.)
                client = boto3.client('bedrock-runtime', region_name=region)
            
            return client
            
        except Exception as e:
            print(f"Error creating Bedrock client: {e}")
            raise
    
    def set_environment_variables(self):
        """Set AWS credentials as environment variables."""
        if not self.credentials:
            self.load_bedrock_credentials()
        
        if not self.credentials:
            print("No credentials to set")
            return False
        
        try:
            if 'aws_access_key_id' in self.credentials:
                os.environ['AWS_ACCESS_KEY_ID'] = self.credentials['aws_access_key_id']
                
            if 'aws_secret_access_key' in self.credentials:
                os.environ['AWS_SECRET_ACCESS_KEY'] = self.credentials['aws_secret_access_key']
                
            if 'aws_session_token' in self.credentials:
                os.environ['AWS_SESSION_TOKEN'] = self.credentials['aws_session_token']
            
            os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
            print("Bedrock credentials set as environment variables")
            return True
            
        except Exception as e:
            print(f"Error setting environment variables: {e}")
            return False
    
    def test_bedrock_access(self, model_id="amazon.titan-text-express-v1"):
        """Test Bedrock access with a simple model invocation."""
        try:
            client = self.create_bedrock_client()
            
            # Test with a simple prompt
            body = {
                "inputText": "Hello, this is a test.",
                "textGenerationConfig": {
                    "maxTokenCount": 10,
                    "temperature": 0.1
                }
            }
            
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            print(f"✅ Bedrock access successful with model: {model_id}")
            return True
            
        except ClientError as e:
            print(f"❌ Bedrock access failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Error testing Bedrock access: {e}")
            return False

def main():
    """Main function to demonstrate usage."""
    print("🔐 Bedrock Credentials Handler")
    print("="*50)
    
    # Initialize handler
    handler = BedrockCredentialsHandler()
    
    # Load credentials
    print("📋 Loading credentials from bedrock.json...")
    creds = handler.load_bedrock_credentials()
    
    if creds:
        print("✅ Credentials loaded successfully")
        print(f"   Available keys: {list(creds.keys())}")
        
        # Set environment variables
        print("\n🌍 Setting environment variables...")
        handler.set_environment_variables()
        
        # Test Bedrock access
        print("\n🧪 Testing Bedrock access...")
        handler.test_bedrock_access()
        
        # Create client for use
        print("\n🚀 Creating Bedrock client...")
        try:
            client = handler.create_bedrock_client()
            print("✅ Bedrock client created successfully")
            print("   You can now use this client for Bedrock operations")
        except Exception as e:
            print(f"❌ Failed to create Bedrock client: {e}")
    else:
        print("❌ Failed to load credentials")

if __name__ == "__main__":
    main()
