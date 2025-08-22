#!/usr/bin/env python3
"""
Simple test script for deepagents tools - tests basic functionality and imports
"""

import sys
import os
import tempfile
import traceback
from pathlib import Path

# Add deepagents to path
sys.path.insert(0, '/home/ec2-user/deepagents')

def test_imports():
    """Test that all tools can be imported successfully"""
    try:
        from deepagents.tools import (
            register_file, write_todos, read_file, edit_file, undo_edit,
            execute_code, python_repl, read_image, think, get_data_dictionary, ls
        )
        from deepagents.state import Todo, DeepAgentState
        print("✅ All tools imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_data_files():
    """Test that data files exist and are accessible"""
    data_files = [
        "/home/ec2-user/deepagents/data/order_data.csv",
        "/home/ec2-user/deepagents/data/cartadds_data.csv", 
        "/home/ec2-user/deepagents/data/clicks_data_trimmed.csv",
        "/home/ec2-user/deepagents/data/impression_data_sample.csv",
        "/home/ec2-user/deepagents/data/catalog.csv"
    ]
    
    missing_files = []
    for file_path in data_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing data files: {missing_files}")
        return False
    else:
        print("✅ All data files exist and are accessible")
        return True

def test_data_loading():
    """Test that data files can be loaded with pandas"""
    try:
        import pandas as pd
        
        data_files = {
            "order_data": "/home/ec2-user/deepagents/data/order_data.csv",
            "cart_adds": "/home/ec2-user/deepagents/data/cartadds_data.csv",
            "clicks": "/home/ec2-user/deepagents/data/clicks_data_trimmed.csv",
            "impression": "/home/ec2-user/deepagents/data/impression_data_sample.csv",
            "catalog": "/home/ec2-user/deepagents/data/catalog.csv"
        }
        
        loaded_files = {}
        for name, path in data_files.items():
            try:
                df = pd.read_csv(path)
                loaded_files[name] = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'size_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
                }
            except Exception as e:
                print(f"❌ Failed to load {name}: {e}")
                return False
        
        print("✅ All data files loaded successfully:")
        for name, info in loaded_files.items():
            print(f"   - {name}: {info['rows']} rows, {info['columns']} cols, {info['size_mb']} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False

def test_tool_definitions():
    """Test that tools are properly defined with correct decorators"""
    try:
        from deepagents.tools import (
            register_file, write_todos, read_file, edit_file, undo_edit,
            execute_code, python_repl, read_image, think, get_data_dictionary
        )
        
        tools = [
            register_file, write_todos, read_file, edit_file, undo_edit,
            execute_code, python_repl, read_image, think, get_data_dictionary
        ]
        
        tool_info = []
        for tool in tools:
            # Check if it has the tool decorator attributes
            has_name = hasattr(tool, 'name')
            has_description = hasattr(tool, 'description') 
            has_args_schema = hasattr(tool, 'args_schema')
            
            # Get the actual name
            tool_name = getattr(tool, 'name', getattr(tool, '__name__', str(tool)))
            
            tool_info.append({
                'name': tool_name,
                'has_name': has_name,
                'has_description': has_description,
                'has_args_schema': has_args_schema,
                'is_tool': has_name or has_description  # Basic check for tool decorator
            })
        
        print("✅ Tool definitions analysis:")
        for info in tool_info:
            status = "✅" if info['is_tool'] else "⚠️"
            print(f"   {status} {info['name']}: name={info['has_name']}, desc={info['has_description']}, schema={info['has_args_schema']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool definition test failed: {e}")
        return False

def test_state_classes():
    """Test that state classes are properly defined"""
    try:
        from deepagents.state import Todo, DeepAgentState
        
        # Test Todo creation (it's a TypedDict)
        todo = Todo(content="Test task", status="pending")
        print(f"✅ Todo TypedDict works: {todo['content']} ({todo['status']})")
        
        # Test DeepAgentState creation
        state = DeepAgentState(messages=[], files={})
        print(f"✅ DeepAgentState class works: {type(state)}")
        
        return True
        
    except Exception as e:
        print(f"❌ State classes test failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        import boto3
        from langchain_core.tools import tool
        from langgraph.types import Command
        from langchain_core.messages import ToolMessage
        
        print("✅ All required dependencies are available")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    print("🧪 Testing DeepAgents Tools - Basic Functionality")
    print("="*60)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Files Test", test_data_files), 
        ("Data Loading Test", test_data_loading),
        ("Tool Definitions Test", test_tool_definitions),
        ("State Classes Test", test_state_classes),
        ("Dependencies Test", test_dependencies)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {passed + failed}")
    print(f"Success Rate: {(passed/(passed + failed)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! The deepagents tools are properly configured.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the output above for details.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
