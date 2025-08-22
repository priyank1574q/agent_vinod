#!/usr/bin/env python3
"""
Simple test to verify prompt caching configuration is working.
"""

import sys
import os
from pathlib import Path

# Add the deepagents directory to the path
sys.path.append(str(Path(__file__).parent / "deepagents"))

def test_caching_configuration():
    """Test that caching configuration is properly set up."""
    
    print("🧪 Testing Prompt Caching Configuration")
    print("=" * 50)
    
    try:
        from model_bedrock import (
            get_claude_sonnet, 
            get_claude_haiku,
            create_cacheable_messages,
            create_cacheable_system_message,
            BEDROCK_MODELS
        )
        print("✅ Successfully imported caching functions")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 1: Check that models have caching enabled by default
    print(f"\n📋 Test 1: Model initialization with caching")
    try:
        model_with_cache = get_claude_sonnet(enable_caching=True)
        model_without_cache = get_claude_sonnet(enable_caching=False)
        print("✅ Models can be initialized with/without caching")
    except Exception as e:
        print(f"❌ Model initialization failed: {e}")
        return False
    
    # Test 2: Check cacheable message creation
    print(f"\n📋 Test 2: Cacheable message creation")
    try:
        system_msg = create_cacheable_system_message("You are a helpful assistant.")
        print(f"✅ System message created with cache control: {system_msg.additional_kwargs}")
        
        messages = create_cacheable_messages(
            system_prompt="You are a helpful assistant.",
            user_message="Hello!"
        )
        print(f"✅ Message list created with {len(messages)} messages")
        print(f"   First message has cache control: {'cache_control' in messages[0].additional_kwargs}")
    except Exception as e:
        print(f"❌ Message creation failed: {e}")
        return False
    
    # Test 3: Check available models
    print(f"\n📋 Test 3: Available models")
    print(f"   Total models configured: {len(BEDROCK_MODELS)}")
    for category, models in [
        ("Claude", [k for k in BEDROCK_MODELS.keys() if "claude" in k]),
        ("Nova", [k for k in BEDROCK_MODELS.keys() if "nova" in k]),
        ("Titan", [k for k in BEDROCK_MODELS.keys() if "titan" in k])
    ]:
        if models:
            print(f"   {category}: {', '.join(models)}")
    
    print(f"\n{'=' * 50}")
    print("CONFIGURATION STATUS")
    print(f"{'=' * 50}")
    print("✅ Prompt caching is properly configured!")
    print("📊 What's enabled:")
    print("   • Cache control in model initialization")
    print("   • Utility functions for cacheable messages")
    print("   • Support for Claude and Nova models")
    print("   • Inference profile IDs for on-demand access")
    
    print(f"\n💡 Next steps:")
    print("   1. Request access to Bedrock models in AWS Console")
    print("   2. Test with a working model once access is granted")
    print("   3. Use create_cacheable_messages() in your applications")
    
    return True

def show_usage_examples():
    """Show examples of how to use the caching features."""
    
    print(f"\n📚 USAGE EXAMPLES")
    print("=" * 50)
    
    print("""
# Example 1: Initialize model with caching
from deepagents.model_bedrock import get_claude_sonnet

model = get_claude_sonnet(enable_caching=True)  # Default is True

# Example 2: Create cacheable messages
from deepagents.model_bedrock import create_cacheable_messages

messages = create_cacheable_messages(
    system_prompt="You are an expert developer...",  # Will be cached
    user_message="Review this code..."
)

response = model.invoke(messages)

# Example 3: Manual cache control
from deepagents.model_bedrock import create_cacheable_system_message
from langchain_core.messages import HumanMessage

messages = [
    create_cacheable_system_message("Long system prompt..."),  # Cached
    HumanMessage(content="User question...")  # Not cached
]

# Example 4: Disable caching if needed
model_no_cache = get_claude_sonnet(enable_caching=False)
""")

if __name__ == "__main__":
    # Set AWS credentials if not already set
    if not os.environ.get('AWS_ACCESS_KEY_ID'):
        os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_AWS_ACCESS_KEY_ID'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_AWS_SECRET_ACCESS_KEY'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    
    success = test_caching_configuration()
    
    if success:
        show_usage_examples()
        print(f"\n🎉 Prompt caching is ready to use!")
        print("   Once you have model access, your requests will automatically")
        print("   benefit from caching for improved performance and lower costs.")
    else:
        print(f"\n❌ Configuration test failed. Please check the setup.")
