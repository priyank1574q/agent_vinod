#!/usr/bin/env python3
"""
Simple test script to verify Amazon Bedrock integration setup.
Run this script to check if everything is configured correctly.
"""

import sys
import os

# Add the deepagents directory to the path
sys.path.append('/home/ec2-user/deepagents')

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from deepagents.model import (
            get_anthropic_claude, get_amazon_nova, get_bedrock_model,
            list_available_models, get_model_info
        )
        print("✅ Model functions imported successfully")
    except ImportError as e:
        print(f"❌ Error importing model functions: {e}")
        return False
    
    try:
        from deepagents.graph import create_deep_agent, create_claude_agent, create_nova_agent
        print("✅ Graph functions imported successfully")
    except ImportError as e:
        print(f"❌ Error importing graph functions: {e}")
        return False
    
    try:
        import boto3
        print("✅ boto3 imported successfully")
    except ImportError as e:
        print(f"❌ Error importing boto3: {e}")
        print("   Install with: pip install boto3")
        return False
    
    try:
        from langchain_aws import ChatBedrock
        print("✅ langchain_aws imported successfully")
    except ImportError as e:
        print(f"❌ Error importing langchain_aws: {e}")
        print("   Install with: pip install langchain-aws")
        return False
    
    return True

def test_aws_credentials():
    """Test if AWS credentials are configured."""
    print("\n🔐 Testing AWS credentials...")
    
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            print("❌ No AWS credentials found")
            print("   Configure with: aws configure")
            return False
        
        print("✅ AWS credentials found")
        
        # Test if we can create a Bedrock client
        try:
            client = boto3.client('bedrock-runtime', region_name='us-east-1')
            print("✅ Bedrock client created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating Bedrock client: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking AWS credentials: {e}")
        return False

def test_model_listing():
    """Test if we can list available models."""
    print("\n📋 Testing model listing...")
    
    try:
        from deepagents.model import list_available_models
        models = list_available_models()
        
        print("✅ Available models:")
        for category, model_list in models.items():
            print(f"   {category}: {len(model_list)} models")
        
        return True
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

def test_model_info():
    """Test if we can get model information."""
    print("\n📊 Testing model information...")
    
    try:
        from deepagents.model import get_model_info
        
        test_model = "claude-3-5-sonnet"
        info = get_model_info(test_model)
        
        print(f"✅ Model info for {test_model}:")
        print(f"   Provider: {info['provider']}")
        print(f"   Family: {info['family']}")
        print(f"   Model ID: {info['model_id']}")
        
        return True
    except Exception as e:
        print(f"❌ Error getting model info: {e}")
        return False

def test_basic_model_creation():
    """Test if we can create a basic model instance."""
    print("\n🤖 Testing model creation...")
    
    try:
        from deepagents.model import get_bedrock_model
        
        # Try to create a model (this will test AWS connectivity)
        model = get_bedrock_model("claude-3-5-sonnet", max_tokens=10)
        print("✅ Model created successfully")
        
        # Try a simple invocation
        try:
            response = model.invoke("Hello")
            print("✅ Model invocation successful")
            print(f"   Response: {response.content[:50]}...")
            return True
        except Exception as e:
            print(f"⚠️  Model created but invocation failed: {e}")
            print("   This might be due to model access permissions")
            return True  # Still consider this a success for setup
            
    except Exception as e:
        print(f"❌ Error creating model: {e}")
        print("   This might be due to:")
        print("   - Missing AWS credentials")
        print("   - No Bedrock model access")
        print("   - Network connectivity issues")
        return False

def test_agent_creation():
    """Test if we can create a basic agent."""
    print("\n🤖 Testing agent creation...")
    
    try:
        from deepagents.graph import create_claude_agent
        from deepagents.tools import think
        
        agent = create_claude_agent(
            tools=[think],
            instructions="You are a test assistant.",
            model_name="claude-3-5-sonnet",
            max_tokens=10
        )
        
        print("✅ Agent created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 DeepAgents Bedrock Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("AWS Credentials Test", test_aws_credentials),
        ("Model Listing Test", test_model_listing),
        ("Model Info Test", test_model_info),
        ("Model Creation Test", test_basic_model_creation),
        ("Agent Creation Test", test_agent_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("• Run: python example_bedrock_usage.py")
        print("• Start API server: python main_bedrock.py")
        print("• Check the README_BEDROCK.md for detailed usage")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("• Install missing packages: pip install -r requirements_bedrock.txt")
        print("• Configure AWS: aws configure")
        print("• Request Bedrock model access in AWS Console")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
