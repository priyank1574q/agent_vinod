# DeepAgents with Amazon Bedrock Integration

Enhanced deepagents framework with support for Amazon Bedrock models including Anthropic Claude and Amazon Nova.

## 🚀 Features

- **Amazon Bedrock Integration**: Native support for Anthropic Claude and Amazon Nova models
- **Backward Compatibility**: Maintains compatibility with existing Azure OpenAI implementations
- **Multiple Model Support**: Easy switching between different LLM providers
- **Enhanced Tools**: Rich set of tools for file operations, code execution, and data analysis
- **FastAPI Server**: Ready-to-use API server with streaming support
- **Comprehensive Examples**: Detailed examples and demonstrations

## 📋 Prerequisites

1. **AWS Account** with access to Amazon Bedrock
2. **AWS CLI** configured with appropriate credentials
3. **Python 3.9+**
4. **Required Python packages** (see requirements_bedrock.txt)

## 🛠️ Installation

1. **Install dependencies:**
```bash
pip install -r requirements_bedrock.txt
```

2. **Configure AWS credentials:**
```bash
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

3. **Ensure Bedrock model access:**
   - Go to AWS Console → Amazon Bedrock → Model access
   - Request access to desired models (Claude, Nova, etc.)

## 🎯 Quick Start

### Basic Model Usage

```python
from deepagents.model import get_anthropic_claude, get_amazon_nova

# Initialize Claude 3.5 Sonnet
claude = get_anthropic_claude("claude-3-5-sonnet", temperature=0.0, max_tokens=1000)
response = claude.invoke("Hello, how are you?")
print(response.content)

# Initialize Amazon Nova Pro
nova = get_amazon_nova("nova-pro", temperature=0.0, max_tokens=1000)
response = nova.invoke("Explain quantum computing briefly.")
print(response.content)
```

### Agent Creation

```python
from deepagents.graph import create_claude_agent, create_nova_agent
from deepagents.tools import think, python_repl, write_file, read_file

tools = [think, python_repl, write_file, read_file]
instructions = "You are a helpful AI assistant with coding capabilities."

# Create Claude agent
claude_agent = create_claude_agent(
    tools=tools,
    instructions=instructions,
    model_name="claude-3-5-sonnet",
    temperature=0.0,
    max_tokens=2000
)

# Create Nova agent
nova_agent = create_nova_agent(
    tools=tools,
    instructions=instructions,
    model_name="nova-pro",
    temperature=0.0,
    max_tokens=2000
)
```

### Using the Agent

```python
import asyncio
from langgraph.checkpoint.memory import InMemorySaver

async def chat_with_agent():
    checkpointer = InMemorySaver()
    
    agent = create_claude_agent(
        tools=[think, python_repl],
        instructions="You are a helpful coding assistant.",
        checkpointer=checkpointer
    )
    
    messages = [{
        "role": "user",
        "content": "Write a Python function to calculate fibonacci numbers."
    }]
    
    config = {"configurable": {"thread_id": "user_123"}}
    
    async for chunk in agent.astream({"messages": messages}, config=config):
        print(chunk)

# Run the async function
asyncio.run(chat_with_agent())
```

## 🌐 FastAPI Server

Start the enhanced API server with Bedrock support:

```bash
python main_bedrock.py
```

The server will be available at `http://localhost:8000` with the following endpoints:

### API Endpoints

- **GET /** - API information and available endpoints
- **GET /health** - Health check
- **GET /models** - List all available Bedrock models
- **GET /models/{model_name}** - Get information about a specific model
- **POST /invoke** - Interact with an agent
- **POST /invoke/stream** - Stream responses from an agent
- **POST /test-model** - Test connection to a specific model

### Example API Usage

```bash
# List available models
curl http://localhost:8000/models

# Get model information
curl http://localhost:8000/models/claude-3-5-sonnet

# Chat with Claude
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model_type": "claude-3-5-sonnet",
    "temperature": 0.0,
    "max_tokens": 1000
  }'

# Chat with Nova
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Explain AI briefly"}],
    "model_type": "nova-pro",
    "temperature": 0.1,
    "max_tokens": 500
  }'
```

## 🔧 Available Models

### Anthropic Claude Models
- `claude-3-5-sonnet` - Most capable, best for complex reasoning
- `claude-3-5-haiku` - Fast and efficient, good for simple tasks
- `claude-3-opus` - Previous generation, very capable
- `claude-3-sonnet` - Previous generation, balanced
- `claude-3-haiku` - Previous generation, fast

### Amazon Nova Models
- `nova-pro` - High-performance multimodal model
- `nova-lite` - Efficient model for common tasks
- `nova-micro` - Ultra-fast model for simple tasks

### Meta Llama Models (also available)
- `llama-3-2-90b` - Large parameter model
- `llama-3-2-11b` - Medium parameter model
- `llama-3-2-3b` - Small parameter model
- `llama-3-2-1b` - Tiny parameter model

## 🛠️ Available Tools

The framework includes a comprehensive set of tools:

### File Operations
- `register_file` - Register a file for processing
- `write_file` - Write content to a file
- `read_file` - Read content from a file
- `ls` - List directory contents
- `edit_file` - Edit existing files
- `undo_edit` - Undo file edits

### Code Execution
- `python_repl` - Execute Python code safely
- `execute_code` - Execute code with output capture

### Task Management
- `write_todos` - Create and manage todo lists
- `think` - Internal reasoning tool

### Data Analysis
- `get_data_dictionary` - Analyze data structure
- `read_image` - Process image files

## 📊 Model Comparison

| Model | Provider | Speed | Capability | Cost | Best For |
|-------|----------|-------|------------|------|----------|
| claude-3-5-sonnet | Anthropic | Medium | Highest | High | Complex reasoning, coding |
| claude-3-5-haiku | Anthropic | Fast | High | Medium | Quick tasks, analysis |
| nova-pro | Amazon | Medium | High | Medium | Multimodal tasks |
| nova-lite | Amazon | Fast | Medium | Low | Simple tasks, chat |
| nova-micro | Amazon | Very Fast | Basic | Very Low | Basic queries |

## 🔍 Examples and Demonstrations

Run the comprehensive example script:

```bash
python example_bedrock_usage.py
```

This script demonstrates:
- Model information and capabilities
- Basic model testing
- Agent creation methods
- Agent interactions
- Advanced tool usage
- File operations and code execution

## 🔧 Configuration Options

### Model Parameters

```python
# Temperature: Controls randomness (0.0 = deterministic, 1.0 = very random)
# Max tokens: Maximum response length
# Region: AWS region for Bedrock

model = get_anthropic_claude(
    model_name="claude-3-5-sonnet",
    temperature=0.0,        # Deterministic responses
    max_tokens=4096,        # Long responses allowed
    region_name="us-east-1", # AWS region
    profile_name=None       # AWS profile (optional)
)
```

### Agent Configuration

```python
agent = create_claude_agent(
    tools=tools,                    # List of available tools
    instructions=instructions,      # System prompt
    model_name="claude-3-5-sonnet", # Model to use
    temperature=0.0,               # Model temperature
    max_tokens=4096,               # Max response length
    checkpointer=checkpointer,     # State persistence
    subagents=[],                  # Sub-agents (optional)
    interrupt_config=None          # Interruption handling
)
```

## 🚨 Error Handling

The framework includes comprehensive error handling:

```python
from deepagents.model import get_bedrock_model

try:
    model = get_bedrock_model("claude-3-5-sonnet")
    response = model.invoke("Hello!")
except ValueError as e:
    print(f"Invalid model configuration: {e}")
except Exception as e:
    print(f"Model error: {e}")
```

## 🔐 Security Considerations

1. **AWS Credentials**: Store securely, use IAM roles when possible
2. **Model Access**: Ensure proper Bedrock model permissions
3. **Code Execution**: The `python_repl` tool executes code - use with caution
4. **File Operations**: Tools can read/write files - validate inputs
5. **API Security**: Add authentication for production deployments

## 📈 Performance Tips

1. **Model Selection**: Choose the right model for your task
   - Use `nova-micro` for simple queries
   - Use `claude-3-5-sonnet` for complex reasoning
   - Use `nova-pro` for multimodal tasks

2. **Token Management**: Set appropriate `max_tokens` limits
3. **Temperature Settings**: Use 0.0 for deterministic tasks, higher for creative tasks
4. **Caching**: Use checkpointers to maintain conversation state
5. **Streaming**: Use streaming endpoints for real-time responses

## 🐛 Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   ```bash
   aws configure
   # OR
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   ```

2. **Model Access Denied**
   - Check Bedrock model access in AWS Console
   - Ensure your AWS account has Bedrock permissions

3. **Import Errors**
   ```bash
   pip install -r requirements_bedrock.txt
   ```

4. **Connection Timeouts**
   - Check your internet connection
   - Verify AWS region settings
   - Try a different AWS region

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project maintains the same license as the original deepagents framework.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Test with the provided demo script
4. Check AWS Bedrock documentation
5. Open an issue with detailed error information

---

**Happy coding with DeepAgents and Amazon Bedrock! 🚀**
