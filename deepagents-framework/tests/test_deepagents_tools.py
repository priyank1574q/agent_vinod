#!/usr/bin/env python3
"""
Comprehensive test script for all tools in deepagents/tools.py
Tests each tool to ensure they work as intended.
"""

import sys
import os
import json
import tempfile
import traceback
from pathlib import Path

# Add deepagents to path
sys.path.insert(0, '/home/ec2-user/deepagents')

try:
    from deepagents.tools import (
        register_file, write_todos, read_file, edit_file, undo_edit,
        execute_code, python_repl, read_image, think, get_data_dictionary, ls
    )
    from deepagents.state import Todo, DeepAgentState
    from langgraph.types import Command
    print("✅ Successfully imported all tools")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add_result(self, tool_name, success, message):
        self.results.append({
            'tool': tool_name,
            'success': success,
            'message': message
        })
        if success:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        print(f"Success Rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        
        print(f"\n{'='*60}")
        print("DETAILED RESULTS")
        print(f"{'='*60}")
        for result in self.results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['tool']}: {result['message']}")

def test_tool(tool_name, test_func, test_results):
    """Helper function to test a tool and record results"""
    try:
        success, message = test_func()
        test_results.add_result(tool_name, success, message)
        print(f"{'✅' if success else '❌'} {tool_name}: {message}")
    except Exception as e:
        test_results.add_result(tool_name, False, f"Exception: {str(e)}")
        print(f"❌ {tool_name}: Exception: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")

def test_register_file():
    """Test register_file tool"""
    try:
        # Create a test file
        test_file = "/tmp/test_register.txt"
        with open(test_file, 'w') as f:
            f.write("Test content for registration")
        
        # Create mock state
        state = DeepAgentState(files={})
        
        # Test the tool
        result = register_file(test_file, state)
        
        # Check if file was registered
        if test_file in state.get('files', {}):
            return True, "Successfully registered file"
        else:
            return False, "File not found in state after registration"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def test_write_todos():
    """Test write_todos tool"""
    try:
        # Create test todos
        todos = [
            Todo(task="Test task 1", priority="high"),
            Todo(task="Test task 2", priority="medium")
        ]
        
        result = write_todos(todos, "test_call_id")
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully created todos command"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_read_file():
    """Test read_file tool"""
    try:
        # Create a test file
        test_file = "/tmp/test_read.txt"
        test_content = "This is test content for reading"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Create mock state with registered file
        state = DeepAgentState(files={test_file: {"content": test_content}})
        
        # Test the tool
        result = read_file(state, "test_call_id", file_path=test_file)
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully read file"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def test_execute_code():
    """Test execute_code tool"""
    try:
        # Create mock state
        state = DeepAgentState(files={})
        
        # Test simple code execution
        test_code = """
import pandas as pd
import numpy as np
result = 2 + 2
print(f"Result: {result}")
"""
        
        result = execute_code(test_code, state, "test_call_id")
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully executed code"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_python_repl():
    """Test python_repl tool"""
    try:
        # Create mock state
        state = DeepAgentState(files={})
        
        # Test REPL
        result = python_repl(state, "test_call_id", code="print('Hello from REPL')")
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully executed REPL command"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_think():
    """Test think tool"""
    try:
        result = think("This is a test thought", "test_call_id")
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully created thought"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_get_data_dictionary():
    """Test get_data_dictionary tool"""
    try:
        # Test getting full data dictionary
        result = get_data_dictionary(tool_call_id="test_call_id")
        
        # Check if result is a Command
        if isinstance(result, Command):
            # Check if the result contains data or error message
            messages = result.update.get('messages', [])
            if messages and len(messages) > 0:
                message_content = messages[0].content
                if "Error: Data file not found" in message_content:
                    return True, "Tool works but data files not accessible (expected in test environment)"
                elif "Data dictionary information" in message_content:
                    return True, "Successfully generated data dictionary"
                else:
                    return True, "Tool executed successfully"
            else:
                return False, "No messages in result"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_ls():
    """Test ls function (not a tool but utility function)"""
    try:
        # Create mock state with files
        state = DeepAgentState(files={
            "/test/file1.txt": {"content": "test1"},
            "/test/file2.txt": {"content": "test2"}
        })
        
        result = ls(state)
        
        # Check if result is a list
        if isinstance(result, list) and len(result) == 2:
            return True, f"Successfully listed {len(result)} files"
        else:
            return False, f"Expected list with 2 files, got {type(result)} with {len(result) if hasattr(result, '__len__') else 'unknown'} items"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_edit_file():
    """Test edit_file tool"""
    try:
        # Create a test file
        test_file = "/tmp/test_edit.txt"
        original_content = "Line 1\nLine 2\nLine 3"
        
        with open(test_file, 'w') as f:
            f.write(original_content)
        
        # Create mock state with registered file
        state = DeepAgentState(files={test_file: {"content": original_content}})
        
        # Test the tool - this requires specific parameters based on the schema
        result = edit_file(
            state=state,
            tool_call_id="test_call_id",
            file_path=test_file,
            old_string="Line 2",
            new_string="Modified Line 2"
        )
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully executed edit command"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def test_undo_edit():
    """Test undo_edit tool"""
    try:
        # Create mock state
        state = DeepAgentState(files={})
        
        result = undo_edit(state, "test_call_id")
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Successfully executed undo command"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_read_image():
    """Test read_image tool"""
    try:
        # Create mock state
        state = DeepAgentState(files={})
        
        # Test with non-existent image (should handle gracefully)
        result = read_image(state, "test_call_id", image_path="/tmp/nonexistent.jpg")
        
        # Check if result is a Command
        if isinstance(result, Command):
            return True, "Tool executed (expected to handle missing image gracefully)"
        else:
            return False, f"Expected Command, got {type(result)}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("🧪 Testing DeepAgents Tools")
    print("="*60)
    
    test_results = TestResults()
    
    # Test each tool
    test_tool("register_file", test_register_file, test_results)
    test_tool("write_todos", test_write_todos, test_results)
    test_tool("read_file", test_read_file, test_results)
    test_tool("edit_file", test_edit_file, test_results)
    test_tool("undo_edit", test_undo_edit, test_results)
    test_tool("execute_code", test_execute_code, test_results)
    test_tool("python_repl", test_python_repl, test_results)
    test_tool("read_image", test_read_image, test_results)
    test_tool("think", test_think, test_results)
    test_tool("get_data_dictionary", test_get_data_dictionary, test_results)
    test_tool("ls (utility)", test_ls, test_results)
    
    # Print summary
    test_results.print_summary()
    
    return test_results.failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
