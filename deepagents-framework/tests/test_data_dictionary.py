#!/usr/bin/env python3
"""
Test script specifically for the get_data_dictionary tool
"""

import sys
import os
import json

# Add deepagents to path
sys.path.insert(0, '/home/ec2-user/deepagents')

def test_data_dictionary_tool():
    """Test the get_data_dictionary tool functionality"""
    try:
        # Import required modules
        from deepagents.tools import get_data_dictionary
        from langgraph.types import Command
        
        print("🧪 Testing get_data_dictionary tool...")
        
        # Test 1: Get full data dictionary
        print("\n📋 Test 1: Getting full data dictionary...")
        result = get_data_dictionary.invoke({"tool_call_id": "test_full"})
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Full data dictionary retrieved successfully")
                
                # Check if it contains expected tables
                if "order_data" in content and "catalog" in content:
                    print("✅ Contains expected table names")
                else:
                    print("⚠️  May not contain all expected tables")
                
                # Try to extract JSON from the content
                try:
                    # Find JSON content between ```json and ```
                    start = content.find("```json\n") + 8
                    end = content.find("\n```", start)
                    if start > 7 and end > start:
                        json_content = content[start:end]
                        data_dict = json.loads(json_content)
                        print(f"✅ Valid JSON structure with {len(data_dict)} tables")
                        
                        # Show table summary
                        for table_name, table_schema in data_dict.items():
                            if isinstance(table_schema, dict):
                                print(f"   - {table_name}: {len(table_schema)} columns")
                            else:
                                print(f"   - {table_name}: {table_schema}")
                    else:
                        print("⚠️  Could not extract JSON content")
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON parsing failed: {e}")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        # Test 2: Get specific table schema
        print("\n📋 Test 2: Getting specific table schema (order_data)...")
        result = get_data_dictionary.invoke({
            "table_name": "order_data",
            "tool_call_id": "test_table"
        })
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Table-specific schema retrieved successfully")
                
                # Check if it contains order_data specific info
                if "order_purchased_date" in content or "product_id" in content:
                    print("✅ Contains expected order_data columns")
                else:
                    print("⚠️  May not contain expected order_data columns")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        # Test 3: Get specific column definition
        print("\n📋 Test 3: Getting specific column definition (order_data.product_id)...")
        result = get_data_dictionary.invoke({
            "table_name": "order_data",
            "column_name": "product_id", 
            "tool_call_id": "test_column"
        })
        
        if isinstance(result, Command):
            messages = result.update.get('messages', [])
            if messages:
                content = messages[0].content
                print("✅ Column-specific definition retrieved successfully")
                
                # Check if it contains product_id specific info
                if "product_id" in content:
                    print("✅ Contains product_id information")
                else:
                    print("⚠️  May not contain product_id information")
            else:
                print("❌ No messages in result")
                return False
        else:
            print(f"❌ Expected Command, got {type(result)}")
            return False
        
        print("\n🎉 All data dictionary tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Data dictionary test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_files_content():
    """Test that data files have expected content structure"""
    try:
        import pandas as pd
        
        print("\n🧪 Testing data file content structure...")
        
        data_files = {
            "order_data": "/home/ec2-user/deepagents/data/order_data.csv",
            "cart_adds": "/home/ec2-user/deepagents/data/cartadds_data.csv",
            "clicks": "/home/ec2-user/deepagents/data/clicks_data_trimmed.csv",
            "impression": "/home/ec2-user/deepagents/data/impression_data_sample.csv",
            "catalog": "/home/ec2-user/deepagents/data/catalog.csv"
        }
        
        expected_columns = {
            "order_data": ["product_id", "customer_id", "order_id"],
            "cart_adds": ["product_id", "customer_id", "session_id"],
            "clicks": ["product_id", "customer_id", "session_id"],
            "impression": ["product_id", "customer_id", "session_id"],
            "catalog": ["product_id", "brand", "title"]
        }
        
        for name, path in data_files.items():
            print(f"\n📋 Checking {name}...")
            df = pd.read_csv(path)
            
            # Check if expected columns exist
            expected_cols = expected_columns.get(name, [])
            missing_cols = [col for col in expected_cols if col not in df.columns]
            
            if missing_cols:
                print(f"⚠️  Missing expected columns: {missing_cols}")
            else:
                print(f"✅ All expected columns present")
            
            # Show basic info
            print(f"   - Shape: {df.shape}")
            print(f"   - Columns: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
            
            # Check for common join columns
            join_cols = ["product_id", "customer_id"]
            available_joins = [col for col in join_cols if col in df.columns]
            print(f"   - Available join columns: {available_joins}")
        
        print("\n✅ Data file content structure check completed")
        return True
        
    except Exception as e:
        print(f"❌ Data file content test failed: {e}")
        return False

def main():
    print("🧪 Testing DeepAgents Data Dictionary Tool")
    print("="*60)
    
    tests = [
        ("Data Dictionary Tool", test_data_dictionary_tool),
        ("Data Files Content", test_data_files_content)
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
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
