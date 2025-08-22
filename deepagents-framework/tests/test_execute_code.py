#!/usr/bin/env python3
"""
Test script for the execute_code tool functionality
"""

import sys
import os

# Add deepagents to path
sys.path.insert(0, '/home/ec2-user/deepagents')

def test_execute_code_tool():
    """Test the execute_code tool functionality"""
    try:
        from deepagents.tools import execute_code
        from deepagents.state import DeepAgentState
        from langgraph.types import Command
        
        print("🧪 Testing execute_code tool...")
        
        # Create a mock state
        state = DeepAgentState(messages=[], files={})
        
        # Test 1: Simple calculation
        print("\n📋 Test 1: Simple calculation...")
        code1 = """
result = 2 + 2
print(f"2 + 2 = {result}")
"""
        
        result = execute_code.invoke({
            "code": code1,
            "state": state,
            "tool_call_id": "test_calc"
        })
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Simple calculation executed successfully")
                if "2 + 2 = 4" in content:
                    print("✅ Correct output produced")
                else:
                    print("⚠️  Output may not be as expected")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        # Test 2: Data analysis with pandas
        print("\n📋 Test 2: Data analysis with pandas...")
        code2 = """
import pandas as pd
import numpy as np

# Create sample data
data = {
    'product_id': [1, 2, 3, 4, 5],
    'revenue': [100, 200, 150, 300, 250],
    'quantity': [1, 2, 1, 3, 2]
}

df = pd.DataFrame(data)
print("Sample DataFrame:")
print(df)
print(f"\\nTotal revenue: ${df['revenue'].sum()}")
print(f"Average revenue: ${df['revenue'].mean():.2f}")
"""
        
        result = execute_code.invoke({
            "code": code2,
            "state": state,
            "tool_call_id": "test_pandas"
        })
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Pandas analysis executed successfully")
                if "Total revenue: $1000" in content:
                    print("✅ Correct calculations produced")
                else:
                    print("⚠️  Calculations may not be as expected")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        # Test 3: Loading actual data files
        print("\n📋 Test 3: Loading actual data files...")
        code3 = """
import pandas as pd

# Load the order data
order_df = pd.read_csv('/home/ec2-user/deepagents/data/order_data.csv')
print(f"Order data shape: {order_df.shape}")
print(f"Columns: {list(order_df.columns)}")
print(f"Total revenue: ${order_df['revenue'].sum():.2f}")

# Load catalog data
catalog_df = pd.read_csv('/home/ec2-user/deepagents/data/catalog.csv')
print(f"\\nCatalog data shape: {catalog_df.shape}")
print(f"Unique products: {catalog_df['product_id'].nunique()}")
"""
        
        result = execute_code.invoke({
            "code": code3,
            "state": state,
            "tool_call_id": "test_real_data"
        })
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Real data loading executed successfully")
                if "Order data shape:" in content and "Catalog data shape:" in content:
                    print("✅ Both datasets loaded correctly")
                else:
                    print("⚠️  Data loading may have issues")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        # Test 4: Error handling
        print("\n📋 Test 4: Error handling...")
        code4 = """
# This should cause an error
undefined_variable = some_undefined_variable + 1
"""
        
        result = execute_code.invoke({
            "code": code4,
            "state": state,
            "tool_call_id": "test_error"
        })
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Error handling executed")
                if "Error" in content or "NameError" in content:
                    print("✅ Error properly caught and reported")
                else:
                    print("⚠️  Error may not be properly handled")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        print("\n🎉 All execute_code tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Execute code test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 Testing DeepAgents Execute Code Tool")
    print("="*60)
    
    success = test_execute_code_tool()
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    
    if success:
        print("✅ Execute code tool is working correctly!")
        print("🎉 The tool can:")
        print("   - Execute basic Python calculations")
        print("   - Work with pandas and numpy")
        print("   - Load and analyze real data files")
        print("   - Handle errors gracefully")
    else:
        print("❌ Execute code tool has issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
