#!/usr/bin/env python3
"""
Example script demonstrating how to use the enhanced deepagents framework 
with Amazon Bedrock models (Anthropic Claude and Amazon Nova).
"""

import asyncio
import os
import sys
from typing import Dict, Any

# Add the deepagents directory to the path
sys.path.append('/home/ec2-user/deepagents')

from deepagents.model import (
    get_anthropic_claude,
    get_amazon_nova,
    get_bedrock_model,
    list_available_models,
    get_model_info,
    get_claude_sonnet,
    get_nova_pro
)
from deepagents.graph import create_deep_agent, create_claude_agent, create_nova_agent
from deepagents.tools import (
    write_todos, write_file, read_file, ls, edit_file, think, 
    execute_code, register_file, python_repl
)
from langgraph.checkpoint.memory import InMemorySaver

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")

async def demonstrate_model_info():
    """Demonstrate model information and listing capabilities."""
    print_section("AVAILABLE BEDROCK MODELS")
    
    try:
        models = list_available_models()
        for category, model_list in models.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for model in model_list:
                print(f"  • {model}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return

    print_subsection("Model Information Examples")
    
    # Show info for a few key models
    example_models = ["claude-3-5-sonnet", "nova-pro", "claude-3-5-haiku", "nova-lite"]
    
    for model_name in example_models:
        try:
            info = get_model_info(model_name)
            print(f"\n{model_name}:")
            print(f"  Provider: {info['provider']}")
            print(f"  Family: {info['family']}")
            print(f"  Model ID: {info['model_id']}")
            print(f"  Function Calling: {info['supports_function_calling']}")
        except Exception as e:
            print(f"  ❌ Error getting info for {model_name}: {e}")

async def test_basic_model_functionality():
    """Test basic model functionality without agents."""
    print_section("BASIC MODEL TESTING")
    
    test_prompt = "Hello! Please respond with a brief greeting and confirm you're working correctly."
    
    models_to_test = [
        ("Claude 3.5 Sonnet", "claude-3-5-sonnet"),
        ("Claude 3.5 Haiku", "claude-3-5-haiku"),
        ("Nova Pro", "nova-pro"),
        ("Nova Lite", "nova-lite")
    ]
    
    for model_display_name, model_name in models_to_test:
        print_subsection(f"Testing {model_display_name}")
        
        try:
            model = get_bedrock_model(model_name, max_tokens=100, temperature=0.1)
            response = model.invoke(test_prompt)
            print(f"✅ {model_display_name} Response:")
            print(f"   {response.content[:200]}...")
        except Exception as e:
            print(f"❌ {model_display_name} Error: {e}")

async def demonstrate_agent_creation():
    """Demonstrate different ways to create agents with Bedrock models."""
    print_section("AGENT CREATION EXAMPLES")
    
    # Basic tools for the agents
    basic_tools = [think, python_repl]
    instructions = """
    You are a helpful AI assistant with access to various tools. 
    Use the tools available to help users with their requests.
    Always think through problems step by step.
    """
    
    checkpointer = InMemorySaver()
    
    print_subsection("Method 1: Using create_claude_agent")
    try:
        claude_agent = create_claude_agent(
            tools=basic_tools,
            instructions=instructions,
            model_name="claude-3-5-sonnet",
            temperature=0.0,
            max_tokens=1000,
            checkpointer=checkpointer
        )
        print("✅ Claude agent created successfully")
    except Exception as e:
        print(f"❌ Error creating Claude agent: {e}")
        claude_agent = None
    
    print_subsection("Method 2: Using create_nova_agent")
    try:
        nova_agent = create_nova_agent(
            tools=basic_tools,
            instructions=instructions,
            model_name="nova-pro",
            temperature=0.0,
            max_tokens=1000,
            checkpointer=checkpointer
        )
        print("✅ Nova agent created successfully")
    except Exception as e:
        print(f"❌ Error creating Nova agent: {e}")
        nova_agent = None
    
    print_subsection("Method 3: Using create_deep_agent with Bedrock")
    try:
        bedrock_agent = create_deep_agent(
            tools=basic_tools,
            instructions=instructions,
            use_bedrock=True,
            bedrock_model_name="claude-3-5-haiku",
            temperature=0.0,
            max_tokens=1000,
            checkpointer=checkpointer
        )
        print("✅ Generic Bedrock agent created successfully")
    except Exception as e:
        print(f"❌ Error creating Bedrock agent: {e}")
        bedrock_agent = None
    
    return claude_agent, nova_agent, bedrock_agent

async def test_agent_interactions(agents):
    """Test agent interactions with simple tasks."""
    print_section("AGENT INTERACTION TESTING")
    
    claude_agent, nova_agent, bedrock_agent = agents
    
    test_message = {
        "messages": [{
            "role": "user", 
            "content": "Calculate the sum of squares for numbers 1 through 5. Show your work step by step."
        }]
    }
    
    agent_tests = [
        ("Claude 3.5 Sonnet Agent", claude_agent),
        ("Nova Pro Agent", nova_agent),
        ("Claude 3.5 Haiku Agent", bedrock_agent)
    ]
    
    for agent_name, agent in agent_tests:
        if agent is None:
            print(f"\n❌ {agent_name}: Not available (creation failed)")
            continue
            
        print_subsection(f"Testing {agent_name}")
        
        try:
            # Use a simple thread ID for testing
            config = {"configurable": {"thread_id": f"test_{agent_name.lower().replace(' ', '_')}"}}
            
            response = ""
            async for chunk in agent.astream(test_message, config=config):
                response = chunk  # Get the final response
            
            print(f"✅ {agent_name} Response:")
            # Print first part of response to avoid too much output
            if hasattr(response, 'get') and 'messages' in response:
                last_message = response['messages'][-1]
                if hasattr(last_message, 'content'):
                    content = last_message.content[:300]
                    print(f"   {content}...")
                else:
                    print(f"   {str(last_message)[:300]}...")
            else:
                print(f"   {str(response)[:300]}...")
                
        except Exception as e:
            print(f"❌ {agent_name} Error: {e}")

async def demonstrate_advanced_features():
    """Demonstrate advanced features like tool usage and file operations."""
    print_section("ADVANCED FEATURES DEMONSTRATION")
    
    # Create an agent with more tools
    advanced_tools = [
        think, python_repl, write_file, read_file, ls, 
        write_todos, register_file
    ]
    
    instructions = """
    You are an advanced AI assistant with access to file operations and code execution.
    When working with files, always register them first before reading.
    Use todos to track your progress on complex tasks.
    Execute code safely using the python_repl tool.
    """
    
    try:
        advanced_agent = create_claude_agent(
            tools=advanced_tools,
            instructions=instructions,
            model_name="claude-3-5-sonnet",
            temperature=0.0,
            max_tokens=2000,
            checkpointer=InMemorySaver()
        )
        
        print("✅ Advanced agent created with full tool suite")
        
        # Test with a complex task
        complex_task = {
            "messages": [{
                "role": "user",
                "content": """
                Please help me with the following task:
                1. Create a simple Python script that generates a list of prime numbers up to 50
                2. Save this script to a file called 'prime_numbers.py'
                3. Execute the script to verify it works
                4. Create a todo list to track this work
                
                Work through this step by step.
                """
            }]
        }
        
        config = {"configurable": {"thread_id": "advanced_test"}}
        
        print_subsection("Executing Complex Task")
        print("Task: Create, save, and execute a prime numbers script")
        
        final_response = ""
        async for chunk in advanced_agent.astream(complex_task, config=config):
            final_response = chunk
        
        print("✅ Complex task completed")
        print("   Check the output above for detailed execution steps")
        
    except Exception as e:
        print(f"❌ Error in advanced features demo: {e}")

async def main():
    """Main function to run all demonstrations."""
    print("🚀 DeepAgents Amazon Bedrock Integration Demo")
    print("=" * 60)
    
    try:
        # 1. Show available models and their info
        await demonstrate_model_info()
        
        # 2. Test basic model functionality
        await test_basic_model_functionality()
        
        # 3. Demonstrate agent creation
        agents = await demonstrate_agent_creation()
        
        # 4. Test agent interactions
        await test_agent_interactions(agents)
        
        # 5. Demonstrate advanced features
        await demonstrate_advanced_features()
        
        print_section("DEMO COMPLETED SUCCESSFULLY")
        print("✅ All demonstrations completed!")
        print("\nNext steps:")
        print("• Run the FastAPI server: python main_bedrock.py")
        print("• Test the API endpoints at http://localhost:8000/docs")
        print("• Integrate with your applications using the enhanced model functions")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Check if we're in an environment that supports asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error running demo: {e}")
        print("\nTry running individual functions or check your AWS credentials.")
        print("Make sure you have:")
        print("1. AWS credentials configured (aws configure)")
        print("2. Access to Amazon Bedrock models")
        print("3. Required Python packages installed")
