"""
Enhanced model.py with Amazon Bedrock support for Anthropic Claude and Amazon Nova models.
Maintains backward compatibility with existing Azure OpenAI implementation.
"""

import os
import boto3
from typing import Optional, Dict, Any, Union
from langchain_aws import ChatBedrock
from langchain_openai import AzureChatOpenAI
from langchain_core.language_models import LanguageModelLike

# Amazon Bedrock Model IDs
BEDROCK_MODELS = {
    # Anthropic Claude Models
    "claude-3-5-sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "claude-3-5-haiku": "anthropic.claude-3-5-haiku-20241022-v1:0", 
    "claude-3-opus": "anthropic.claude-3-opus-20240229-v1:0",
    "claude-3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "claude-3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    
    # Amazon Nova Models
    "nova-pro": "amazon.nova-pro-v1:0",
    "nova-lite": "amazon.nova-lite-v1:0",
    "nova-micro": "amazon.nova-micro-v1:0",
    
    # Meta Llama Models (for completeness)
    "llama-3-2-90b": "meta.llama3-2-90b-instruct-v1:0",
    "llama-3-2-11b": "meta.llama3-2-11b-instruct-v1:0",
    "llama-3-2-3b": "meta.llama3-2-3b-instruct-v1:0",
    "llama-3-2-1b": "meta.llama3-2-1b-instruct-v1:0",
}

def get_bedrock_client(region_name: str = "us-east-1", profile_name: Optional[str] = None) -> boto3.client:
    """
    Initialize and return a Bedrock client.
    
    Args:
        region_name: AWS region name (default: us-east-1)
        profile_name: AWS profile name (optional)
    
    Returns:
        boto3.client: Configured Bedrock client
    """
    session = boto3.Session(profile_name=profile_name) if profile_name else boto3.Session()
    return session.client("bedrock-runtime", region_name=region_name)

def get_anthropic_claude(
    model_name: str = "claude-3-5-sonnet",
    temperature: float = 0.0,
    max_tokens: int = 4096,
    region_name: str = "us-east-1",
    profile_name: Optional[str] = None,
    **kwargs
) -> ChatBedrock:
    """
    Initialize Anthropic Claude model via Amazon Bedrock.
    
    Args:
        model_name: Claude model name (claude-3-5-sonnet, claude-3-5-haiku, etc.)
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        region_name: AWS region name
        profile_name: AWS profile name (optional)
        **kwargs: Additional model parameters
    
    Returns:
        ChatBedrock: Configured Claude model
    """
    if model_name not in BEDROCK_MODELS:
        available_models = [k for k in BEDROCK_MODELS.keys() if k.startswith("claude")]
        raise ValueError(f"Invalid Claude model: {model_name}. Available: {available_models}")
    
    model_id = BEDROCK_MODELS[model_name]
    
    # Claude-specific model parameters
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        **kwargs
    }
    
    return ChatBedrock(
        model_id=model_id,
        model_kwargs=model_kwargs,
        region_name=region_name,
        credentials_profile_name=profile_name,
    )

def get_amazon_nova(
    model_name: str = "nova-pro",
    temperature: float = 0.0,
    max_tokens: int = 4096,
    region_name: str = "us-east-1",
    profile_name: Optional[str] = None,
    **kwargs
) -> ChatBedrock:
    """
    Initialize Amazon Nova model via Amazon Bedrock.
    
    Args:
        model_name: Nova model name (nova-pro, nova-lite, nova-micro)
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        region_name: AWS region name
        profile_name: AWS profile name (optional)
        **kwargs: Additional model parameters
    
    Returns:
        ChatBedrock: Configured Nova model
    """
    if model_name not in BEDROCK_MODELS:
        available_models = [k for k in BEDROCK_MODELS.keys() if k.startswith("nova")]
        raise ValueError(f"Invalid Nova model: {model_name}. Available: {available_models}")
    
    model_id = BEDROCK_MODELS[model_name]
    
    # Nova-specific model parameters
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        **kwargs
    }
    
    return ChatBedrock(
        model_id=model_id,
        model_kwargs=model_kwargs,
        region_name=region_name,
        credentials_profile_name=profile_name,
    )

def get_bedrock_model(
    model_name: str,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    region_name: str = "us-east-1",
    profile_name: Optional[str] = None,
    **kwargs
) -> ChatBedrock:
    """
    Generic function to get any Bedrock model.
    
    Args:
        model_name: Model name from BEDROCK_MODELS
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        region_name: AWS region name
        profile_name: AWS profile name (optional)
        **kwargs: Additional model parameters
    
    Returns:
        ChatBedrock: Configured model
    """
    if model_name not in BEDROCK_MODELS:
        raise ValueError(f"Invalid model: {model_name}. Available: {list(BEDROCK_MODELS.keys())}")
    
    model_id = BEDROCK_MODELS[model_name]
    
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        **kwargs
    }
    
    return ChatBedrock(
        model_id=model_id,
        model_kwargs=model_kwargs,
        region_name=region_name,
        credentials_profile_name=profile_name,
    )

# Original function with enhanced capabilities
def get_default_model(
    loaded_creds: Optional[Dict[str, Any]] = None,
    temperature: float = 0.0,
    max_tokens: int = 2048,
    use_bedrock: bool = False,
    model_name: str = "claude-3-5-sonnet"
) -> Union[AzureChatOpenAI, ChatBedrock]:
    """
    Get the default model. Can return either Azure OpenAI or Bedrock model.
    
    Args:
        loaded_creds: Azure OpenAI credentials (for backward compatibility)
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        use_bedrock: Whether to use Bedrock instead of Azure OpenAI
        model_name: Bedrock model name (if use_bedrock=True)
    
    Returns:
        Union[AzureChatOpenAI, ChatBedrock]: Configured model
    """
    if use_bedrock:
        return get_bedrock_model(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    # Original Azure OpenAI implementation
    if not loaded_creds:
        raise ValueError("loaded_creds required for Azure OpenAI model")
    
    return AzureChatOpenAI(
        azure_endpoint=loaded_creds["azure_endpoint"],
        openai_api_version=loaded_creds["openai_api_version"],
        deployment_name=loaded_creds["deployment_name"],
        openai_api_key=loaded_creds["openai_api_key"],
        openai_api_type=loaded_creds["openai_api_type"],
        temperature=temperature,
        max_tokens=max_tokens
    )

# Convenience functions for specific model families
def get_claude_sonnet(temperature: float = 0.0, max_tokens: int = 4096, **kwargs) -> ChatBedrock:
    """Get Claude 3.5 Sonnet model."""
    return get_anthropic_claude("claude-3-5-sonnet", temperature, max_tokens, **kwargs)

def get_claude_haiku(temperature: float = 0.0, max_tokens: int = 4096, **kwargs) -> ChatBedrock:
    """Get Claude 3.5 Haiku model."""
    return get_anthropic_claude("claude-3-5-haiku", temperature, max_tokens, **kwargs)

def get_nova_pro(temperature: float = 0.0, max_tokens: int = 4096, **kwargs) -> ChatBedrock:
    """Get Amazon Nova Pro model."""
    return get_amazon_nova("nova-pro", temperature, max_tokens, **kwargs)

def get_nova_lite(temperature: float = 0.0, max_tokens: int = 4096, **kwargs) -> ChatBedrock:
    """Get Amazon Nova Lite model."""
    return get_amazon_nova("nova-lite", temperature, max_tokens, **kwargs)

def get_nova_micro(temperature: float = 0.0, max_tokens: int = 4096, **kwargs) -> ChatBedrock:
    """Get Amazon Nova Micro model."""
    return get_amazon_nova("nova-micro", temperature, max_tokens, **kwargs)

# Model selection helper
def list_available_models() -> Dict[str, list]:
    """
    List all available models by category.
    
    Returns:
        Dict[str, list]: Dictionary of model categories and their available models
    """
    return {
        "anthropic_claude": [k for k in BEDROCK_MODELS.keys() if k.startswith("claude")],
        "amazon_nova": [k for k in BEDROCK_MODELS.keys() if k.startswith("nova")],
        "meta_llama": [k for k in BEDROCK_MODELS.keys() if k.startswith("llama")],
        "all_models": list(BEDROCK_MODELS.keys())
    }

def get_model_info(model_name: str) -> Dict[str, Any]:
    """
    Get information about a specific model.
    
    Args:
        model_name: Model name
    
    Returns:
        Dict[str, Any]: Model information
    """
    if model_name not in BEDROCK_MODELS:
        raise ValueError(f"Model {model_name} not found")
    
    model_id = BEDROCK_MODELS[model_name]
    
    # Extract model family and provider
    if "anthropic" in model_id:
        provider = "Anthropic"
        family = "Claude"
    elif "amazon" in model_id:
        provider = "Amazon"
        family = "Nova"
    elif "meta" in model_id:
        provider = "Meta"
        family = "Llama"
    else:
        provider = "Unknown"
        family = "Unknown"
    
    return {
        "name": model_name,
        "model_id": model_id,
        "provider": provider,
        "family": family,
        "supports_streaming": True,
        "supports_function_calling": True if provider in ["Anthropic", "Amazon"] else False
    }

# Legacy compatibility - keeping original commented functions
# def get_gemini(temperature=0.0,max_tokens=512):
#     vertexai.init(project=PROJECT_ID, location="us-central1",credentials=credentials)
#     llm = ChatVertexAI(
#   project=PROJECT_ID, model_name="gemini-2.0-flash-001" ,# "gemini-1.5-flash-001"
#   location="us-central1", credentials=credentials, max_output_tokens=256,
#   temperature=0, top_p=1, timeout=120, max_retries=4
# )
#     return llm
