#!/usr/bin/env python3
"""
Quick test to verify the fixed Claude 3.5 model IDs work with inference profiles
"""

import json
from bedrock_credentials_handler import BedrockCredentialsHandler
from botocore.exceptions import ClientError

def test_fixed_claude_models():
    """Test the fixed Claude 3.5 models using inference profiles"""
    
    print("🔧 Testing Fixed Claude 3.5 Models with Inference Profiles")
    print("=" * 60)
    
    # Initialize handler
    handler = BedrockCredentialsHandler()
    
    # Load credentials
    if not handler.load_bedrock_credentials():
        print("❌ Failed to load credentials from bedrock.json")
        return
    
    # Create Bedrock client
    bedrock = handler.create_bedrock_client()
    
    # Test the problematic models with correct inference profile IDs
    test_models = {
        "Claude 3.5 Haiku (US Profile)": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "Claude 3.5 Sonnet (US Profile)": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "Claude 3 Opus (US Profile)": "us.anthropic.claude-3-opus-20240229-v1:0",
    }
    
    for model_name, model_id in test_models.items():
        print(f"\n🧪 Testing {model_name}...")
        print(f"   Model ID: {model_id}")
        
        try:
            # Test with Claude format
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 50,
                "messages": [{"role": "user", "content": "Hello! Please respond with 'Model working correctly.'"}],
                "temperature": 0.1
            }
            
            response = bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text']
            
            print(f"   ✅ SUCCESS - Response: {response_text[:100]}...")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"   ❌ FAILED - {error_code}: {error_message}")
            
        except Exception as e:
            print(f"   ❌ ERROR - {str(e)}")
    
    print(f"\n{'='*60}")
    print("✅ Test completed! The models above should now work in your Streamlit app.")

if __name__ == "__main__":
    test_fixed_claude_models()
