"""
Simplified Amazon Bedrock integration for Streamlit app.
This module provides easy access to Bedrock models without requiring the full deepagents framework.
"""

import boto3
import streamlit as st
from typing import Optional, Dict, Any, List
from langchain_aws import ChatBedrock
import json
import os

# Amazon Bedrock Model IDs (Updated with correct inference profiles)
BEDROCK_MODELS = {
    # Amazon Titan Models (WORKING)
    "Titan Text G1 - Express": "amazon.titan-text-express-v1",
    "Titan Text G1 - Lite": "amazon.titan-text-lite-v1",
    
    # Anthropic Claude Models (WORKING - Legacy versions)
    "Claude 3 Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "Claude 3 Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    
    # Anthropic Claude Models (Using Inference Profiles - FIXED)
    "Claude 3.5 Haiku": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "Claude 3.5 Sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "Claude 3 Opus": "us.anthropic.claude-3-opus-20240229-v1:0",
    
    # Alternative inference profiles for different regions
    "Claude 3.5 Haiku (EU)": "eu.anthropic.claude-3-5-haiku-20241022-v1:0",
    "Claude 3.5 Sonnet (EU)": "eu.anthropic.claude-3-5-sonnet-20241022-v2:0",
    
    # Amazon Nova Models (may require special access)
    "Nova Pro": "amazon.nova-pro-v1:0",
    "Nova Lite": "amazon.nova-lite-v1:0",
    "Nova Micro": "amazon.nova-micro-v1:0",
    
    # Meta Llama Models
    "Llama 3.2 90B": "meta.llama3-2-90b-instruct-v1:0",
    "Llama 3.2 11B": "meta.llama3-2-11b-instruct-v1:0",
    "Llama 3.2 3B": "meta.llama3-2-3b-instruct-v1:0",
    "Llama 3.2 1B": "meta.llama3-2-1b-instruct-v1:0",
}

# Model categories for UI organization (prioritizing working models)
MODEL_CATEGORIES = {
    "Amazon Titan (✅ Working)": [
        "Titan Text G1 - Express", "Titan Text G1 - Lite"
    ],
    "Anthropic Claude (✅ Working)": [
        "Claude 3 Haiku", "Claude 3 Sonnet", "Claude 3.5 Haiku", "Claude 3.5 Sonnet"
    ],
    "Anthropic Claude (🌍 Regional)": [
        "Claude 3.5 Haiku (EU)", "Claude 3.5 Sonnet (EU)", "Claude 3 Opus"
    ],
    "Amazon Nova (⚠️ May Need Access)": [
        "Nova Pro", "Nova Lite", "Nova Micro"
    ],
    "Meta Llama (⚠️ May Need Access)": [
        "Llama 3.2 90B", "Llama 3.2 11B", "Llama 3.2 3B", "Llama 3.2 1B"
    ]
}

# Model information for display
MODEL_INFO = {
    "Claude 3.5 Sonnet": {
        "provider": "Anthropic",
        "description": "Most capable model, excellent for complex reasoning and coding",
        "speed": "Medium",
        "cost": "High",
        "best_for": "Complex analysis, coding, creative writing"
    },
    "Claude 3.5 Haiku": {
        "provider": "Anthropic", 
        "description": "Fast and efficient, good for quick tasks",
        "speed": "Fast",
        "cost": "Low",
        "best_for": "Quick questions, simple analysis, chat"
    },
    "Claude 3 Haiku (Legacy)": {
        "provider": "Anthropic", 
        "description": "Legacy version, widely available",
        "speed": "Fast",
        "cost": "Low",
        "best_for": "Quick questions, simple analysis, chat"
    },
    "Claude 3 Sonnet (Legacy)": {
        "provider": "Anthropic", 
        "description": "Legacy version, widely available",
        "speed": "Medium",
        "cost": "Medium",
        "best_for": "General purpose analysis"
    },
    "Nova Pro": {
        "provider": "Amazon",
        "description": "High-performance multimodal model",
        "speed": "Medium",
        "cost": "Medium",
        "best_for": "Multimodal tasks, general purpose"
    },
    "Nova Lite": {
        "provider": "Amazon",
        "description": "Efficient model for common tasks",
        "speed": "Fast", 
        "cost": "Low",
        "best_for": "Common tasks, quick responses"
    },
    "Nova Micro": {
        "provider": "Amazon",
        "description": "Ultra-fast model for simple tasks",
        "speed": "Very Fast",
        "cost": "Very Low", 
        "best_for": "Simple queries, basic chat"
    },
    "Titan Text G1 - Express": {
        "provider": "Amazon",
        "description": "Fast and cost-effective text generation",
        "speed": "Fast",
        "cost": "Low",
        "best_for": "Text generation, summarization"
    },
    "Titan Text G1 - Lite": {
        "provider": "Amazon",
        "description": "Lightweight model for simple tasks",
        "speed": "Very Fast",
        "cost": "Very Low",
        "best_for": "Simple text tasks, basic analysis"
    },
    "Jurassic-2 Ultra": {
        "provider": "AI21 Labs",
        "description": "Advanced language model for complex tasks",
        "speed": "Medium",
        "cost": "Medium",
        "best_for": "Complex text generation, analysis"
    },
    "Jurassic-2 Mid": {
        "provider": "AI21 Labs",
        "description": "Balanced performance and cost",
        "speed": "Fast",
        "cost": "Low",
        "best_for": "General text tasks, content creation"
    }
}

@st.cache_resource
def get_bedrock_client(region_name: str = "us-east-1") -> Optional[boto3.client]:
    """
    Get a cached Bedrock client.
    
    Args:
        region_name: AWS region name
        
    Returns:
        boto3.client or None if failed
    """
    try:
        return boto3.client("bedrock-runtime", region_name=region_name)
    except Exception as e:
        st.error(f"Failed to create Bedrock client: {e}")
        return None

@st.cache_resource
def create_bedrock_model(
    model_name: str,
    temperature: float = 0.0,
    max_tokens: int = 1000,
    region_name: str = "us-east-1"
) -> Optional[ChatBedrock]:
    """
    Create a cached Bedrock model instance.
    
    Args:
        model_name: Display name of the model
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        region_name: AWS region name
        
    Returns:
        ChatBedrock instance or None if failed
    """
    try:
        if model_name not in BEDROCK_MODELS:
            st.error(f"Model {model_name} not found")
            return None
            
        model_id = BEDROCK_MODELS[model_name]
        
        model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        return ChatBedrock(
            model_id=model_id,
            model_kwargs=model_kwargs,
            region_name=region_name,
        )
    except Exception as e:
        st.error(f"Failed to create model {model_name}: {e}")
        return None

def test_aws_connection() -> bool:
    """
    Test AWS connection and Bedrock access.
    
    Returns:
        bool: True if connection successful
    """
    try:
        client = get_bedrock_client()
        if client is None:
            return False
            
        # Try to list foundation models (this tests permissions)
        response = client.list_foundation_models()
        return True
    except Exception as e:
        st.error(f"AWS connection test failed: {e}")
        return False

def get_available_models() -> List[str]:
    """
    Get list of available models that can be accessed.
    
    Returns:
        List of model names that are accessible
    """
    available = []
    
    # Test a few key models
    test_models = ["Claude 3.5 Haiku", "Nova Micro"]  # Start with fastest/cheapest
    
    for model_name in test_models:
        try:
            model = create_bedrock_model(model_name, max_tokens=10)
            if model is not None:
                # Try a simple invocation to test access
                response = model.invoke("Hi")
                available.extend(list(BEDROCK_MODELS.keys()))
                break  # If one works, assume all work
        except Exception:
            continue
    
    return available if available else list(BEDROCK_MODELS.keys())

def invoke_model(
    model_name: str,
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 1000,
    system_prompt: Optional[str] = None
) -> Optional[str]:
    """
    Invoke a Bedrock model with the given prompt.
    
    Args:
        model_name: Display name of the model
        prompt: User prompt
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system prompt
        
    Returns:
        Model response or None if failed
    """
    try:
        model = create_bedrock_model(model_name, temperature, max_tokens)
        if model is None:
            return None
            
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))
        
        response = model.invoke(messages)
        return response.content
        
    except Exception as e:
        st.error(f"Model invocation failed: {e}")
        return None

def stream_model_response(
    model_name: str,
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 1000,
    system_prompt: Optional[str] = None
):
    """
    Stream response from a Bedrock model.
    
    Args:
        model_name: Display name of the model
        prompt: User prompt
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system prompt
        
    Yields:
        Chunks of the response
    """
    try:
        model = create_bedrock_model(model_name, temperature, max_tokens)
        if model is None:
            yield "Error: Could not create model"
            return
            
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))
        
        for chunk in model.stream(messages):
            yield chunk.content
            
    except Exception as e:
        yield f"Error: {e}"

def get_model_info(model_name: str) -> Dict[str, Any]:
    """
    Get information about a model.
    
    Args:
        model_name: Display name of the model
        
    Returns:
        Dictionary with model information
    """
    return MODEL_INFO.get(model_name, {
        "provider": "Unknown",
        "description": "No description available",
        "speed": "Unknown",
        "cost": "Unknown",
        "best_for": "General purpose"
    })

def format_model_display(model_name: str) -> str:
    """
    Format model name for display with additional info.
    
    Args:
        model_name: Model name
        
    Returns:
        Formatted string for display
    """
    info = get_model_info(model_name)
    return f"{model_name} ({info['provider']}) - {info['speed']} | {info['cost']} cost"

# Utility functions for Streamlit integration
def display_model_info_sidebar():
    """Display model information in the sidebar."""
    st.sidebar.markdown("### 🤖 Available Models")
    
    for category, models in MODEL_CATEGORIES.items():
        with st.sidebar.expander(f"📁 {category}"):
            for model in models:
                info = get_model_info(model)
                st.markdown(f"""
                **{model}**
                - Speed: {info['speed']}
                - Cost: {info['cost']}
                - Best for: {info['best_for']}
                """)

def check_aws_setup() -> bool:
    """
    Check if AWS is properly set up and display status.
    
    Returns:
        bool: True if AWS is properly configured
    """
    st.sidebar.markdown("### 🔧 AWS Status")
    
    # Check AWS credentials
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            st.sidebar.error("❌ No AWS credentials found")
            st.sidebar.markdown("""
            **Setup Instructions:**
            1. Run `aws configure`
            2. Or set environment variables:
               - `AWS_ACCESS_KEY_ID`
               - `AWS_SECRET_ACCESS_KEY`
               - `AWS_DEFAULT_REGION`
            """)
            return False
        else:
            st.sidebar.success("✅ AWS credentials found")
            
    except Exception as e:
        st.sidebar.error(f"❌ AWS setup error: {e}")
        return False
    
    # Check Bedrock access
    try:
        client = get_bedrock_client()
        if client:
            st.sidebar.success("✅ Bedrock client created")
            return True
        else:
            st.sidebar.error("❌ Failed to create Bedrock client")
            return False
    except Exception as e:
        st.sidebar.error(f"❌ Bedrock access error: {e}")
        return False
