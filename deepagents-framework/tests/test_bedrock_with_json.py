#!/usr/bin/env python3
"""
Test script to check Bedrock models using credentials from bedrock.json
"""

import json
from bedrock_credentials_handler import BedrockCredentialsHandler
from botocore.exceptions import ClientError

def test_bedrock_models_with_json():
    """Test which Bedrock models are available using bedrock.json credentials"""
    
    # Initialize credentials handler
    handler = BedrockCredentialsHandler()
    
    # Load credentials
    print("🔐 Loading credentials from bedrock.json...")
    if not handler.load_bedrock_credentials():
        print("❌ Failed to load credentials from bedrock.json")
        return None
    
    print("✅ Credentials loaded successfully")
    
    # Models to test
    test_models = {
        # Amazon Titan (usually widely available)
        "Titan Text Express": "amazon.titan-text-express-v1",
        "Titan Text Lite": "amazon.titan-text-lite-v1",
        
        # Claude models (legacy - direct model IDs)
        "Claude 3 Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
        "Claude 3 Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        
        # Claude models (using inference profiles - FIXED)
        "Claude 3.5 Haiku (US Profile)": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
        "Claude 3.5 Sonnet (US Profile)": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        "Claude 3 Opus (US Profile)": "us.anthropic.claude-3-opus-20240229-v1:0",
        
        # AI21 models
        "Jurassic-2 Mid": "ai21.j2-mid-v1",
        "Jurassic-2 Ultra": "ai21.j2-ultra-v1",
        
        # Nova models
        "Nova Micro": "amazon.nova-micro-v1:0",
        "Nova Lite": "amazon.nova-lite-v1:0",
        "Nova Pro": "amazon.nova-pro-v1:0",
    }
    
    try:
        # Create Bedrock client using credentials from bedrock.json
        bedrock = handler.create_bedrock_client()
        
        print("\n🧪 Testing Bedrock Model Availability")
        print("="*60)
        
        available_models = []
        unavailable_models = []
        
        for model_name, model_id in test_models.items():
            print(f"\n📋 Testing {model_name}...")
            print(f"   Model ID: {model_id}")
            
            try:
                # Try a simple invocation with minimal input
                if "titan" in model_id.lower():
                    # Titan models use different format
                    body = {
                        "inputText": "Hello",
                        "textGenerationConfig": {
                            "maxTokenCount": 10,
                            "temperature": 0.1
                        }
                    }
                elif "ai21" in model_id.lower():
                    # AI21 models use different format
                    body = {
                        "prompt": "Hello",
                        "maxTokens": 10,
                        "temperature": 0.1
                    }
                else:
                    # Anthropic/Claude models
                    body = {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "Hello"}],
                        "temperature": 0.1
                    }
                
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
            
            return recommended[1], handler  # Return model ID and handler
        else:
            print(f"\n❌ No models are available with current credentials")
            return None, handler
            
    except Exception as e:
        print(f"❌ Failed to test models: {e}")
        return None, handler

def create_bedrock_client_example():
    """Example of how to create and use a Bedrock client with bedrock.json"""
    
    print("\n" + "="*60)
    print("EXAMPLE: Creating Bedrock Client")
    print("="*60)
    
    # Method 1: Using the handler class
    handler = BedrockCredentialsHandler()
    
    try:
        client = handler.create_bedrock_client()
        print("✅ Method 1: Created client using BedrockCredentialsHandler")
        
        # Test the client
        body = {
            "inputText": "What is AWS Bedrock?",
            "textGenerationConfig": {
                "maxTokenCount": 50,
                "temperature": 0.7
            }
        }
        
        response = client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=json.dumps(body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        print(f"✅ Test response: {response_body.get('results', [{}])[0].get('outputText', 'No response')[:100]}...")
        
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    # Method 2: Set environment variables and use standard boto3
    print(f"\n📋 Method 2: Setting environment variables...")
    handler.set_environment_variables()
    
    try:
        import boto3
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        print("✅ Method 2: Created client using environment variables")
        
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")

if __name__ == "__main__":
    # Test models with bedrock.json credentials
    recommended_model, handler = test_bedrock_models_with_json()
    
    if recommended_model:
        print(f"\n🚀 You can use model ID: {recommended_model}")
        print("   Update your applications to use this model as the default.")
        
        # Show example usage
        create_bedrock_client_example()
    else:
        print("\n💡 Troubleshooting suggestions:")
        print("   1. Check that bedrock.json contains valid credentials")
        print("   2. Verify Bedrock access permissions")
        print("   3. Try a different AWS region")
        print("   4. Request access to specific models in AWS Console")
        print("   5. Check if the credentials in bedrock.json have expired")
