#!/usr/bin/env python3
"""
Test script to check which Bedrock models are available with proper JSON formatting
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

# Set AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_AWS_ACCESS_KEY_ID'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_AWS_SECRET_ACCESS_KEY'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

def test_bedrock_models():
    """Test which Bedrock models are available"""
    
    # Models to test with proper request formats
    test_models = {
        # Amazon Titan models
        "Titan Text Express": {
            "model_id": "amazon.titan-text-express-v1",
            "body": {
                "inputText": "Hello",
                "textGenerationConfig": {
                    "maxTokenCount": 10,
                    "temperature": 0.1
                }
            }
        },
        "Titan Text Lite": {
            "model_id": "amazon.titan-text-lite-v1",
            "body": {
                "inputText": "Hello",
                "textGenerationConfig": {
                    "maxTokenCount": 10,
                    "temperature": 0.1
                }
            }
        },
        
        # Claude models (legacy)
        "Claude 3 Haiku": {
            "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.1
            }
        },
        "Claude 3 Sonnet": {
            "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
            "body": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "Hello"}],
                "temperature": 0.1
            }
        },
        
        # AI21 models
        "Jurassic-2 Mid": {
            "model_id": "ai21.j2-mid-v1",
            "body": {
                "prompt": "Hello",
                "maxTokens": 10,
                "temperature": 0.1
            }
        },
        
        # Nova models
        "Nova Micro": {
            "model_id": "amazon.nova-micro-v1:0",
            "body": {
                "messages": [{"role": "user", "content": "Hello"}],
                "inferenceConfig": {
                    "maxTokens": 10,
                    "temperature": 0.1
                }
            }
        }
    }
    
    try:
        # Create Bedrock client
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        print("🧪 Testing Bedrock Model Availability (Fixed)")
        print("="*60)
        
        available_models = []
        unavailable_models = []
        
        for model_name, config in test_models.items():
            model_id = config["model_id"]
            body = config["body"]
            
            print(f"\n📋 Testing {model_name}...")
            print(f"   Model ID: {model_id}")
            
            try:
                response = bedrock.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType='application/json'
                )
                
                print(f"   ✅ AVAILABLE - Model responded successfully")
                available_models.append((model_name, model_id))
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                print(f"   ❌ UNAVAILABLE - {error_code}: {error_message}")
                unavailable_models.append((model_name, model_id, f"{error_code}: {error_message}"))
                
            except Exception as e:
                print(f"   ❌ ERROR - {str(e)}")
                unavailable_models.append((model_name, model_id, str(e)))
        
        # Summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Available Models: {len(available_models)}")
        print(f"❌ Unavailable Models: {len(unavailable_models)}")
        
        if available_models:
            print(f"\n🎉 AVAILABLE MODELS:")
            for name, model_id in available_models:
                print(f"   ✅ {name}: {model_id}")
        
        if unavailable_models:
            print(f"\n⚠️  UNAVAILABLE MODELS:")
            for name, model_id, error in unavailable_models:
                print(f"   ❌ {name}: {error}")
        
        # Recommend best model to use
        if available_models:
            recommended = available_models[0]  # First available model
            print(f"\n💡 RECOMMENDATION:")
            print(f"   Use: {recommended[0]}")
            print(f"   Model ID: {recommended[1]}")
            
            return recommended[1]  # Return model ID
        else:
            print(f"\n❌ No models are available with current credentials")
            return None
            
    except Exception as e:
        print(f"❌ Failed to test models: {e}")
        return None

if __name__ == "__main__":
    recommended_model = test_bedrock_models()
    
    if recommended_model:
        print(f"\n🚀 You can use model ID: {recommended_model}")
        print("   Update your Streamlit app to use this model as the default.")
    else:
        print("\n💡 Suggestions:")
        print("   1. Check your AWS credentials")
        print("   2. Verify Bedrock access permissions") 
        print("   3. Try a different AWS region")
        print("   4. Request access to specific models in AWS Console")
