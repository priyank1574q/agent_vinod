#!/bin/bash

echo "🚀 Starting DeepAgents File Analyzer with Amazon Bedrock"
echo "=" * 60

# Check if required files exist
if [ ! -f "app_bedrock.py" ]; then
    echo "❌ app_bedrock.py not found!"
    exit 1
fi

if [ ! -f "bedrock_integration.py" ]; then
    echo "❌ bedrock_integration.py not found!"
    exit 1
fi

echo "✅ Required files found"

# Check Python packages
echo "📦 Checking Python packages..."
python3 -c "import streamlit, pandas, plotly, boto3, langchain_aws" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Required packages installed"
else
    echo "⚠️  Some packages might be missing. Installing..."
    pip install --user streamlit pandas plotly boto3 langchain-aws
fi

# Check AWS credentials
echo "🔐 Checking AWS setup..."
if aws sts get-caller-identity >/dev/null 2>&1; then
    echo "✅ AWS credentials configured"
else
    echo "⚠️  AWS credentials not configured"
    echo "   The app will still run but Bedrock features may not work"
    echo "   Run 'aws configure' to set up credentials"
fi

echo ""
echo "🌐 Starting Streamlit app..."
echo "📊 The app will be available at: http://localhost:8501"
echo "🔗 External access: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'localhost'):8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Streamlit app
streamlit run app_bedrock.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
