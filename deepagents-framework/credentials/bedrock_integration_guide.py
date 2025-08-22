#!/usr/bin/env python3
"""
Integration Guide: How to use bedrock.json credentials in your existing code

This file shows different ways to integrate bedrock.json credentials into your applications.
"""

import json
from bedrock_credentials_handler import BedrockCredentialsHandler

# ============================================================================
# METHOD 1: Direct Integration (Recommended)
# ============================================================================

def method_1_direct_integration():
    """Use the BedrockCredentialsHandler directly in your code"""
    
    print("🔧 METHOD 1: Direct Integration")
    print("-" * 50)
    
    # Initialize handler
    handler = BedrockCredentialsHandler()
    
    # Create Bedrock client
    bedrock_client = handler.create_bedrock_client()
    
    # Use the client
    body = {
        "inputText": "What is machine learning?",
        "textGenerationConfig": {
            "maxTokenCount": 100,
            "temperature": 0.7
        }
    }
    
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=json.dumps(body),
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    text = response_body['results'][0]['outputText']
    
    print(f"✅ Response: {text[:100]}...")
    return bedrock_client

# ============================================================================
# METHOD 2: Environment Variables
# ============================================================================

def method_2_environment_variables():
    """Set environment variables and use standard boto3"""
    
    print("\n🌍 METHOD 2: Environment Variables")
    print("-" * 50)
    
    # Load credentials and set environment variables
    handler = BedrockCredentialsHandler()
    handler.set_environment_variables()
    
    # Now use standard boto3
    import boto3
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Test the client
    body = {
        "inputText": "Hello from environment variables!",
        "textGenerationConfig": {
            "maxTokenCount": 50,
            "temperature": 0.5
        }
    }
    
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=json.dumps(body),
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    text = response_body['results'][0]['outputText']
    
    print(f"✅ Response: {text[:100]}...")
    return bedrock_client

# ============================================================================
# METHOD 3: Class-based Integration
# ============================================================================

class MyBedrockApp:
    """Example class that integrates bedrock.json credentials"""
    
    def __init__(self, bedrock_json_path='/home/ec2-user/bedrock.json'):
        self.handler = BedrockCredentialsHandler(bedrock_json_path)
        self.client = None
        self.initialize()
    
    def initialize(self):
        """Initialize the Bedrock client"""
        try:
            self.client = self.handler.create_bedrock_client()
            print("✅ MyBedrockApp initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
    
    def generate_text(self, prompt, model_id="amazon.titan-text-express-v1", max_tokens=100):
        """Generate text using Bedrock"""
        if not self.client:
            raise ValueError("Bedrock client not initialized")
        
        # Prepare body based on model type
        if "titan" in model_id.lower():
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": 0.7
                }
            }
        elif "claude" in model_id.lower():
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
        
        response = self.client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        
        if "titan" in model_id.lower():
            return response_body['results'][0]['outputText']
        elif "claude" in model_id.lower():
            return response_body['content'][0]['text']
    
    def chat(self, messages, model_id="anthropic.claude-3-haiku-20240307-v1:0"):
        """Multi-turn chat with Claude models"""
        if "claude" not in model_id.lower():
            raise ValueError("Chat method only works with Claude models")
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 200,
            "messages": messages,
            "temperature": 0.7
        }
        
        response = self.client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

def method_3_class_based():
    """Use class-based integration"""
    
    print("\n🏗️ METHOD 3: Class-based Integration")
    print("-" * 50)
    
    # Initialize the app
    app = MyBedrockApp()
    
    # Generate text with Titan
    titan_response = app.generate_text(
        "Explain quantum computing in simple terms",
        model_id="amazon.titan-text-express-v1"
    )
    print(f"✅ Titan Response: {titan_response[:100]}...")
    
    # Chat with Claude
    messages = [
        {"role": "user", "content": "What is the capital of France?"},
    ]
    claude_response = app.chat(messages)
    print(f"✅ Claude Response: {claude_response[:100]}...")

# ============================================================================
# METHOD 4: Function-based Wrapper
# ============================================================================

def create_bedrock_client_from_json(json_path='/home/ec2-user/bedrock.json'):
    """Simple function to create a Bedrock client from bedrock.json"""
    handler = BedrockCredentialsHandler(json_path)
    return handler.create_bedrock_client()

def method_4_function_wrapper():
    """Use simple function wrapper"""
    
    print("\n⚡ METHOD 4: Function Wrapper")
    print("-" * 50)
    
    # Create client with one function call
    client = create_bedrock_client_from_json()
    
    # Use it immediately
    body = {
        "inputText": "Write a haiku about coding",
        "textGenerationConfig": {
            "maxTokenCount": 100,
            "temperature": 0.8
        }
    }
    
    response = client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=json.dumps(body),
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    text = response_body['results'][0]['outputText']
    
    print(f"✅ Haiku Response: {text}")

# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Demonstrate all integration methods"""
    
    print("🚀 BEDROCK.JSON INTEGRATION GUIDE")
    print("=" * 60)
    print("This guide shows 4 different ways to integrate bedrock.json")
    print("credentials into your applications.")
    print("=" * 60)
    
    try:
        # Method 1: Direct integration
        method_1_direct_integration()
        
        # Method 2: Environment variables
        method_2_environment_variables()
        
        # Method 3: Class-based
        method_3_class_based()
        
        # Method 4: Function wrapper
        method_4_function_wrapper()
        
        print("\n" + "=" * 60)
        print("✅ ALL METHODS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n💡 RECOMMENDATIONS:")
        print("   • Use Method 1 for simple scripts")
        print("   • Use Method 2 for existing boto3 code")
        print("   • Use Method 3 for complex applications")
        print("   • Use Method 4 for quick prototypes")
        
        print("\n🎯 AVAILABLE MODELS:")
        print("   • amazon.titan-text-express-v1 (Recommended)")
        print("   • amazon.titan-text-lite-v1")
        print("   • anthropic.claude-3-haiku-20240307-v1:0")
        print("   • anthropic.claude-3-sonnet-20240229-v1:0")
        print("   • us.anthropic.claude-3-5-haiku-20241022-v1:0")
        print("   • us.anthropic.claude-3-5-sonnet-20241022-v2:0")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")

if __name__ == "__main__":
    main()
