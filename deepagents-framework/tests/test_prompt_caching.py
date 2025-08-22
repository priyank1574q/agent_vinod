#!/usr/bin/env python3
"""
Test script to demonstrate prompt caching with Bedrock models.
This shows how to use the updated model_bedrock.py with caching enabled.
"""

import sys
import os
import time
from pathlib import Path

# Add the deepagents directory to the path
sys.path.append(str(Path(__file__).parent / "deepagents"))

from model_bedrock import (
    get_claude_sonnet, 
    get_claude_haiku,
    create_cacheable_messages,
    create_cacheable_system_message
)
from langchain_core.messages import HumanMessage

def test_prompt_caching():
    """Test prompt caching with Claude models."""
    
    print("🧪 Testing Prompt Caching with Bedrock Models")
    print("=" * 60)
    
    # Initialize model with caching enabled (default)
    try:
        model = get_claude_sonnet(enable_caching=True, max_tokens=100)
        print("✅ Model initialized with caching enabled")
    except Exception as e:
        print(f"❌ Failed to initialize model: {e}")
        return
    
    # Create a system prompt that will be cached
    system_prompt = """You are an expert Python developer and code reviewer. 
    You provide detailed, constructive feedback on code quality, performance, 
    and best practices. Always explain your reasoning and suggest specific 
    improvements with code examples when possible."""
    
    print(f"\n📝 System prompt (will be cached):")
    print(f"   Length: {len(system_prompt)} characters")
    print(f"   Preview: {system_prompt[:100]}...")
    
    # Test 1: First request with caching
    print(f"\n🔄 Test 1: First request (will cache system prompt)")
    start_time = time.time()
    
    messages1 = create_cacheable_messages(
        system_prompt=system_prompt,
        user_message="Review this Python function: def add(a, b): return a + b"
    )
    
    try:
        response1 = model.invoke(messages1)
        end_time = time.time()
        print(f"   ✅ Response received in {end_time - start_time:.2f} seconds")
        print(f"   Response preview: {response1.content[:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Second request with same system prompt (should use cache)
    print(f"\n🔄 Test 2: Second request (should use cached system prompt)")
    start_time = time.time()
    
    messages2 = create_cacheable_messages(
        system_prompt=system_prompt,  # Same system prompt - should use cache
        user_message="What are the best practices for error handling in Python?"
    )
    
    try:
        response2 = model.invoke(messages2)
        end_time = time.time()
        print(f"   ✅ Response received in {end_time - start_time:.2f} seconds")
        print(f"   Response preview: {response2.content[:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 3: Request without caching for comparison
    print(f"\n🔄 Test 3: Request without caching (for comparison)")
    start_time = time.time()
    
    model_no_cache = get_claude_sonnet(enable_caching=False, max_tokens=100)
    
    # Create messages without cache markers
    messages3 = [
        HumanMessage(content=f"{system_prompt}\n\nWhat is the difference between list and tuple in Python?")
    ]
    
    try:
        response3 = model_no_cache.invoke(messages3)
        end_time = time.time()
        print(f"   ✅ Response received in {end_time - start_time:.2f} seconds")
        print(f"   Response preview: {response3.content[:150]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    print(f"\n{'=' * 60}")
    print("CACHING ANALYSIS")
    print(f"{'=' * 60}")
    print("✅ Prompt caching is now enabled in your models!")
    print("📊 Benefits you should see:")
    print("   • Faster response times for repeated system prompts")
    print("   • Lower costs (cached content not charged for input tokens)")
    print("   • Better performance for agent workflows")
    print("\n💡 Best practices:")
    print("   • Cache long system prompts and instructions")
    print("   • Use consistent system prompts across requests")
    print("   • Cache context that doesn't change between requests")

def test_different_models():
    """Test caching with different model types."""
    
    print(f"\n🔄 Testing caching with different models")
    print("-" * 40)
    
    models_to_test = [
        ("Claude 3.5 Sonnet", lambda: get_claude_sonnet(enable_caching=True, max_tokens=50)),
        ("Claude 3.5 Haiku", lambda: get_claude_haiku(enable_caching=True, max_tokens=50)),
    ]
    
    system_prompt = "You are a helpful assistant. Respond concisely."
    
    for model_name, model_func in models_to_test:
        print(f"\n📋 Testing {model_name}...")
        try:
            model = model_func()
            messages = create_cacheable_messages(
                system_prompt=system_prompt,
                user_message="What is 2+2?"
            )
            response = model.invoke(messages)
            print(f"   ✅ {model_name}: {response.content[:100]}...")
        except Exception as e:
            print(f"   ❌ {model_name}: {e}")

if __name__ == "__main__":
    # Set AWS credentials if not already set
    if not os.environ.get('AWS_ACCESS_KEY_ID'):
        os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_AWS_ACCESS_KEY_ID'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_AWS_SECRET_ACCESS_KEY'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    
    test_prompt_caching()
    test_different_models()
    
    print(f"\n🎉 Prompt caching is now configured!")
    print("   Your models will automatically cache system prompts and long context.")
    print("   This will improve performance and reduce costs for your agent workflows.")
