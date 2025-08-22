#!/usr/bin/env python3
"""
Test script for Streamlit Bedrock integration.
This script tests the core functionality without running the full Streamlit app.
"""

import sys
import os
from typing import Dict, Any

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        print("✅ Data processing libraries imported")
    except ImportError as e:
        print(f"❌ Data processing import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import boto3
        from langchain_aws import ChatBedrock
        print("✅ AWS and LangChain libraries imported")
    except ImportError as e:
        print(f"❌ AWS/LangChain import failed: {e}")
        return False
    
    try:
        from bedrock_integration import (
            BEDROCK_MODELS, create_bedrock_model, invoke_model
        )
        print("✅ Bedrock integration module imported")
    except ImportError as e:
        print(f"❌ Bedrock integration import failed: {e}")
        return False
    
    return True

def test_bedrock_integration():
    """Test the bedrock integration module."""
    print("\n🤖 Testing Bedrock integration...")
    
    try:
        from bedrock_integration import (
            BEDROCK_MODELS, MODEL_CATEGORIES, MODEL_INFO,
            get_model_info, format_model_display
        )
        
        # Test model information
        test_model = "Claude 3.5 Haiku"
        if test_model in BEDROCK_MODELS:
            info = get_model_info(test_model)
            display_name = format_model_display(test_model)
            print(f"✅ Model info retrieved for {test_model}")
            print(f"   Provider: {info['provider']}")
            print(f"   Display: {display_name}")
        else:
            print(f"⚠️  Test model {test_model} not found in BEDROCK_MODELS")
        
        # Test model categories
        total_models = sum(len(models) for models in MODEL_CATEGORIES.values())
        print(f"✅ Found {total_models} models across {len(MODEL_CATEGORIES)} categories")
        
        return True
    except Exception as e:
        print(f"❌ Bedrock integration test failed: {e}")
        return False

def test_aws_connection():
    """Test AWS connection."""
    print("\n🔐 Testing AWS connection...")
    
    try:
        import boto3
        
        # Check credentials
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            print("❌ No AWS credentials found")
            print("   Run: aws configure")
            return False
        else:
            print("✅ AWS credentials found")
        
        # Try to create Bedrock client
        try:
            client = boto3.client('bedrock-runtime', region_name='us-east-1')
            print("✅ Bedrock client created")
            return True
        except Exception as e:
            print(f"⚠️  Bedrock client creation failed: {e}")
            print("   This might be due to permissions or region issues")
            return False
            
    except Exception as e:
        print(f"❌ AWS connection test failed: {e}")
        return False

def test_model_creation():
    """Test creating a model instance."""
    print("\n🤖 Testing model creation...")
    
    try:
        from bedrock_integration import create_bedrock_model
        
        # Try to create a lightweight model
        model = create_bedrock_model(
            model_name="Claude 3.5 Haiku",
            temperature=0.0,
            max_tokens=50
        )
        
        if model is not None:
            print("✅ Model instance created successfully")
            return True
        else:
            print("❌ Model creation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False

def test_file_processing():
    """Test file processing functions."""
    print("\n📁 Testing file processing...")
    
    try:
        import pandas as pd
        import io
        
        # Create test data
        test_csv_data = """name,age,city
John,25,New York
Jane,30,San Francisco
Bob,35,Chicago"""
        
        test_text_data = "This is a test text file with some sample content for analysis."
        
        # Test CSV processing
        csv_file = io.StringIO(test_csv_data)
        df = pd.read_csv(csv_file)
        print(f"✅ CSV processing: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Test text processing
        text_stats = {
            'characters': len(test_text_data),
            'words': len(test_text_data.split()),
            'lines': len(test_text_data.splitlines())
        }
        print(f"✅ Text processing: {text_stats['characters']} chars, {text_stats['words']} words")
        
        return True
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        return False

def test_visualization():
    """Test visualization capabilities."""
    print("\n📊 Testing visualization...")
    
    try:
        import plotly.express as px
        import pandas as pd
        
        # Create test data
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3],
            'category': ['A', 'B', 'A', 'B', 'A']
        })
        
        # Create test plots
        fig1 = px.scatter(df, x='x', y='y', color='category')
        fig2 = px.histogram(df, x='y')
        
        print("✅ Plotly visualizations created successfully")
        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Streamlit Bedrock Integration Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Bedrock Integration Test", test_bedrock_integration),
        ("AWS Connection Test", test_aws_connection),
        ("Model Creation Test", test_model_creation),
        ("File Processing Test", test_file_processing),
        ("Visualization Test", test_visualization),
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
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Streamlit app is ready to run.")
        print("\nTo start the app:")
        print("  streamlit run app_bedrock.py")
        print("\nThe app will be available at: http://localhost:8501")
    elif passed >= total - 2:  # Allow for AWS connection issues
        print("\n⚠️  Most tests passed. You can try running the app.")
        print("  Some AWS-related features might not work without proper setup.")
        print("\nTo start the app:")
        print("  streamlit run app_bedrock.py")
    else:
        print(f"\n❌ {total - passed} tests failed. Fix issues before running the app.")
        print("\nCommon fixes:")
        print("• Install missing packages: pip install -r requirements.txt")
        print("• Configure AWS: aws configure")
        print("• Check internet connectivity")
    
    return passed >= total - 2  # Allow some AWS issues

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
