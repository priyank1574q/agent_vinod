"""
Enhanced main.py with Amazon Bedrock support for Anthropic Claude and Amazon Nova models.
This demonstrates how to use the updated deepagents framework with Bedrock models.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional, Literal, Union
from typing_extensions import Annotated
from typing_extensions import TypedDict, NotRequired
from datetime import datetime, timedelta
import traceback
import difflib
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

from deepagents.graph import create_deep_agent, create_claude_agent, create_nova_agent
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from typing import Annotated
from langgraph.prebuilt import InjectedState

from deepagents.sub_agent import _create_task_tool, SubAgent
from deepagents.model import (
    get_default_model, 
    get_anthropic_claude, 
    get_amazon_nova, 
    get_bedrock_model,
    list_available_models,
    get_model_info
)
from deepagents.tools import (
    write_todos, write_file, read_file, ls, edit_file, think, 
    execute_code, register_file, python_repl, read_image, 
    undo_edit, get_data_dictionary
)
from deepagents.state import DeepAgentState
from typing import Sequence, Union, Callable, Any, TypeVar, Type, Optional
from langchain_core.tools import BaseTool
from langchain_core.language_models import LanguageModelLike

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
import uuid

app = FastAPI(title="DeepAgents with Amazon Bedrock", version="2.0.0")

# Configuration
extra_tools = [think, execute_code, register_file, python_repl, read_image, undo_edit]
checkpointer = InMemorySaver()

# Base path for outputs
base_path = "/home/ec2-user/deepagents/outputs"
os.makedirs(base_path, exist_ok=True)

# Load coding instructions
prompt_file_path = os.path.join("/home/ec2-user/deepagents/coding_prompt", "coding_prompt_v4.md")

try:
    with open(prompt_file_path, 'r') as f:
        prompt_template = f.read()
    coding_instructions = prompt_template.format(base_path=base_path)
except FileNotFoundError:
    # Fallback instructions if file not found
    coding_instructions = f"""
    You are an advanced AI coding assistant with access to various tools for file manipulation, 
    code execution, and data analysis. Your base working directory is {base_path}.
    
    Always use the available tools to:
    1. Register files before reading them
    2. Write todos to track your progress
    3. Execute code safely using the python_repl tool
    4. Save outputs to the base path directory
    
    Be thorough, accurate, and helpful in your responses.
    """

# Global agent instances
agents = {}

class Request(BaseModel):
    messages: list
    model_type: Optional[str] = "claude-3-5-sonnet"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 4096

class ModelListResponse(BaseModel):
    available_models: Dict[str, List[str]]

class ModelInfoResponse(BaseModel):
    model_info: Dict[str, Any]

def get_or_create_agent(model_type: str, temperature: float = 0.0, max_tokens: int = 4096):
    """Get or create an agent for the specified model type."""
    agent_key = f"{model_type}_{temperature}_{max_tokens}"
    
    if agent_key not in agents:
        try:
            if model_type.startswith("claude"):
                agent = create_claude_agent(
                    tools=extra_tools,
                    instructions=coding_instructions,
                    model_name=model_type,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    checkpointer=checkpointer,
                ).with_config({"recursion_limit": 50})
            elif model_type.startswith("nova"):
                agent = create_nova_agent(
                    tools=extra_tools,
                    instructions=coding_instructions,
                    model_name=model_type,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    checkpointer=checkpointer,
                ).with_config({"recursion_limit": 50})
            else:
                # Generic Bedrock model
                agent = create_deep_agent(
                    tools=extra_tools,
                    instructions=coding_instructions,
                    use_bedrock=True,
                    bedrock_model_name=model_type,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    checkpointer=checkpointer,
                ).with_config({"recursion_limit": 50})
            
            agents[agent_key] = agent
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create agent: {str(e)}")
    
    return agents[agent_key]

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "DeepAgents with Amazon Bedrock API",
        "version": "2.0.0",
        "endpoints": {
            "/invoke": "POST - Interact with the agent",
            "/models": "GET - List available models",
            "/models/{model_name}": "GET - Get model information",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/models", response_model=ModelListResponse)
async def get_available_models():
    """Get list of available Bedrock models."""
    try:
        models = list_available_models()
        return ModelListResponse(available_models=models)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")

@app.get("/models/{model_name}", response_model=ModelInfoResponse)
async def get_model_information(model_name: str):
    """Get information about a specific model."""
    try:
        model_info = get_model_info(model_name)
        return ModelInfoResponse(model_info=model_info)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

@app.post("/invoke")
async def invoke(request: Request):
    """
    Interact with the agent using the specified model.
    
    Args:
        request: Request containing messages and model configuration
    
    Returns:
        Agent response
    """
    try:
        # Get or create agent for the specified model
        agent = get_or_create_agent(
            model_type=request.model_type,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Generate a unique thread ID for this conversation
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        # Process the request
        last_message = ""
        async for s in agent.astream({"messages": request.messages}, config=config):
            last_message = s
        
        return {
            "response": last_message,
            "model_used": request.model_type,
            "thread_id": thread_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent invocation failed: {str(e)}")

@app.post("/invoke/stream")
async def invoke_stream(request: Request):
    """
    Stream responses from the agent.
    
    Args:
        request: Request containing messages and model configuration
    
    Returns:
        Streaming response
    """
    try:
        from fastapi.responses import StreamingResponse
        import json
        
        agent = get_or_create_agent(
            model_type=request.model_type,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        async def generate():
            async for s in agent.astream({"messages": request.messages}, config=config):
                yield f"data: {json.dumps(s)}\n\n"
            yield f"data: [DONE]\n\n"
        
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")

@app.post("/test-model")
async def test_model(model_name: str = "claude-3-5-sonnet"):
    """
    Test connection to a specific Bedrock model.
    
    Args:
        model_name: Name of the model to test
    
    Returns:
        Test result
    """
    try:
        model = get_bedrock_model(model_name, max_tokens=10)
        response = model.invoke("Hello, can you respond with just 'OK'?")
        
        return {
            "model": model_name,
            "status": "success",
            "response": response.content,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "model": model_name,
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Example usage functions
@app.post("/examples/claude-analysis")
async def claude_analysis_example():
    """Example endpoint showing Claude analysis capabilities."""
    try:
        agent = get_or_create_agent("claude-3-5-sonnet")
        
        messages = [{
            "role": "user",
            "content": "Create a simple data analysis example using pandas. Generate some sample data, analyze it, and create a visualization."
        }]
        
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        result = ""
        async for s in agent.astream({"messages": messages}, config=config):
            result = s
        
        return {
            "example": "Claude Data Analysis",
            "result": result,
            "model": "claude-3-5-sonnet"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Example failed: {str(e)}")

@app.post("/examples/nova-coding")
async def nova_coding_example():
    """Example endpoint showing Nova coding capabilities."""
    try:
        agent = get_or_create_agent("nova-pro")
        
        messages = [{
            "role": "user",
            "content": "Write a Python function to calculate fibonacci numbers and demonstrate its usage with some examples."
        }]
        
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        result = ""
        async for s in agent.astream({"messages": messages}, config=config):
            result = s
        
        return {
            "example": "Nova Coding",
            "result": result,
            "model": "nova-pro"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Example failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting DeepAgents with Amazon Bedrock...")
    print("📊 Available models:")
    
    try:
        models = list_available_models()
        for category, model_list in models.items():
            print(f"  {category}: {model_list}")
    except Exception as e:
        print(f"  ⚠️  Could not load models: {e}")
    
    print("\n🌐 Starting server on http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
