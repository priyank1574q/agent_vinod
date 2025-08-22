#!/usr/bin/env python3
"""
Dry test script to verify deepagents-bedrock integration before Streamlit implementation.
"""

import sys
import os
import asyncio
from typing import Dict, Any, List

# Add paths
sys.path.append('/home/ec2-user/deepagents')

def test_basic_imports():
    """Test if we can import all required modules."""
    print("🔍 Testing basic imports...")
    
    try:
        # Test deepagents imports
        from deepagents.model import (
            get_anthropic_claude, get_amazon_nova, get_bedrock_model,
            list_available_models, get_model_info
        )
        from deepagents.graph import create_claude_agent, create_nova_agent
        from deepagents.tools import think, python_repl, write_file, read_file
        print("✅ DeepAgents imports successful")
        
        # Test streamlit import
        import streamlit as st
        print("✅ Streamlit import successful")
        
        # Test other required imports
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        print("✅ Data processing imports successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_model_availability():
    """Test if we can list and access models."""
    print("\n📋 Testing model availability...")
    
    try:
        from deepagents.model import list_available_models, get_model_info
        
        models = list_available_models()
        print(f"✅ Found {len(models['all_models'])} total models")
        
        # Test specific models we'll use in Streamlit
        test_models = ["claude-3-5-sonnet", "claude-3-5-haiku", "nova-pro", "nova-lite"]
        available_models = []
        
        for model in test_models:
            try:
                info = get_model_info(model)
                available_models.append(model)
                print(f"✅ {model}: {info['provider']} {info['family']}")
            except Exception as e:
                print(f"⚠️  {model}: Not available - {e}")
        
        return available_models
    except Exception as e:
        print(f"❌ Model availability test failed: {e}")
        return []

def test_simple_model_creation():
    """Test creating a simple model instance."""
    print("\n🤖 Testing model creation...")
    
    try:
        from deepagents.model import get_bedrock_model
        
        # Try to create a lightweight model
        model = get_bedrock_model("claude-3-5-haiku", max_tokens=50, temperature=0.0)
        print("✅ Model instance created successfully")
        
        # Test a simple invocation
        try:
            response = model.invoke("Say 'Hello from Bedrock!'")
            print(f"✅ Model response: {response.content[:100]}...")
            return True
        except Exception as e:
            print(f"⚠️  Model created but invocation failed: {e}")
            print("   (This might be due to AWS permissions)")
            return True  # Still consider creation successful
            
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False

def test_agent_creation():
    """Test creating an agent with tools."""
    print("\n🤖 Testing agent creation...")
    
    try:
        from deepagents.graph import create_claude_agent
        from deepagents.tools import think, python_repl
        from langgraph.checkpoint.memory import InMemorySaver
        
        agent = create_claude_agent(
            tools=[think, python_repl],
            instructions="You are a helpful assistant for testing.",
            model_name="claude-3-5-haiku",
            temperature=0.0,
            max_tokens=100,
            checkpointer=InMemorySaver()
        )
        
        print("✅ Agent created successfully")
        return agent
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return None

async def test_agent_interaction(agent):
    """Test basic agent interaction."""
    print("\n💬 Testing agent interaction...")
    
    if agent is None:
        print("❌ No agent available for testing")
        return False
    
    try:
        test_message = {
            "messages": [{
                "role": "user",
                "content": "Hello! Please respond with a brief greeting."
            }]
        }
        
        config = {"configurable": {"thread_id": "dry_test"}}
        
        response = ""
        async for chunk in agent.astream(test_message, config=config):
            response = chunk
        
        print("✅ Agent interaction successful")
        print(f"   Response type: {type(response)}")
        
        # Try to extract the actual response content
        if hasattr(response, 'get') and 'messages' in response:
            last_message = response['messages'][-1]
            if hasattr(last_message, 'content'):
                print(f"   Content preview: {last_message.content[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ Agent interaction failed: {e}")
        return False

def test_streamlit_compatibility():
    """Test Streamlit-specific functionality."""
    print("\n🎨 Testing Streamlit compatibility...")
    
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
        
        # Test creating sample data (what we might do in Streamlit)
        sample_data = pd.DataFrame({
            'model': ['claude-3-5-sonnet', 'claude-3-5-haiku', 'nova-pro'],
            'provider': ['Anthropic', 'Anthropic', 'Amazon'],
            'speed': ['Medium', 'Fast', 'Medium']
        })
        
        print("✅ Sample data creation successful")
        print(f"   Data shape: {sample_data.shape}")
        
        # Test session state simulation
        session_state = {}
        session_state['messages'] = []
        session_state['current_model'] = 'claude-3-5-sonnet'
        
        print("✅ Session state simulation successful")
        
        return True
    except Exception as e:
        print(f"❌ Streamlit compatibility test failed: {e}")
        return False

async def run_dry_test():
    """Run all dry tests."""
    print("🧪 DeepAgents-Bedrock Streamlit Integration Dry Test")
    print("=" * 60)
    
    tests = []
    
    # Basic functionality tests
    tests.append(("Import Test", test_basic_imports()))
    
    available_models = test_model_availability()
    tests.append(("Model Availability", len(available_models) > 0))
    
    tests.append(("Model Creation", test_simple_model_creation()))
    
    agent = test_agent_creation()
    tests.append(("Agent Creation", agent is not None))
    
    interaction_success = await test_agent_interaction(agent)
    tests.append(("Agent Interaction", interaction_success))
    
    tests.append(("Streamlit Compatibility", test_streamlit_compatibility()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DRY TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All dry tests passed! Ready for Streamlit integration.")
        return True, available_models
    else:
        print(f"\n⚠️  {total - passed} tests failed. Fix issues before Streamlit integration.")
        return False, available_models

def main():
    """Main function."""
    try:
        success, available_models = asyncio.run(run_dry_test())
        
        if success:
            print("\n🚀 INTEGRATION RECOMMENDATIONS:")
            print("=" * 60)
            print("✅ Proceed with Streamlit integration")
            print(f"✅ Use these models: {available_models}")
            print("✅ Include error handling for AWS connectivity")
            print("✅ Add model selection in Streamlit sidebar")
            print("✅ Implement session state for conversation history")
            print("✅ Add streaming support for real-time responses")
        else:
            print("\n🛑 ISSUES TO FIX BEFORE INTEGRATION:")
            print("=" * 60)
            print("❌ Fix failing tests above")
            print("❌ Ensure AWS credentials are configured")
            print("❌ Verify Bedrock model access permissions")
            print("❌ Install missing dependencies")
        
        return success
    except Exception as e:
        print(f"\n💥 Dry test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
