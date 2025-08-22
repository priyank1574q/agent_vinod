# DeepAgents Framework

A powerful AI agent framework built with LangGraph and Amazon Bedrock for complex data analysis and code generation tasks.

## 🚀 Features

- **Multi-Agent Architecture**: Coordinated agents for different tasks
- **Amazon Bedrock Integration**: Support for Claude, Titan, and other models
- **Advanced Tool System**: File analysis, code execution, data processing
- **Prompt Caching**: Optimized performance with Claude models
- **Flexible Model Support**: Easy switching between different LLM providers

## 📁 Project Structure

```
deepagents-framework/
├── core/
│   ├── __init__.py              # Package initialization
│   ├── graph.py                 # LangGraph workflow definition
│   ├── state.py                 # Agent state management
│   ├── model.py                 # Model abstraction layer
│   ├── model_bedrock.py         # Amazon Bedrock integration
│   ├── tools.py                 # Agent tools and utilities
│   ├── prompts.py               # System prompts and templates
│   ├── sub_agent.py             # Sub-agent implementations
│   └── interrupt.py             # Workflow interruption handling
├── examples/
│   ├── main.py                  # Basic usage example
│   ├── main_bedrock.py          # Bedrock-specific example
│   └── example_bedrock_usage.py # Comprehensive Bedrock demo
├── tests/
│   ├── test_deepagents_tools.py # Tool testing
│   ├── test_data_dictionary.py  # Data analysis tests
│   ├── test_execute_code.py     # Code execution tests
│   └── test_bedrock_setup.py    # Bedrock integration tests
├── credentials/
│   ├── bedrock_credentials_handler.py # Credential management
│   ├── test_bedrock_models.py         # Model availability tests
│   └── bedrock_integration_guide.py   # Integration examples
├── data/                        # Sample datasets
├── coding_prompt/               # Coding prompt templates
├── docs/                        # Documentation
└── requirements_bedrock.txt     # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd deepagents-framework
```

2. **Install dependencies**
```bash
pip install -r requirements_bedrock.txt
```

3. **Set up AWS credentials**
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Option 3: Use bedrock.json (see credentials/bedrock_credentials_handler.py)
```

## 🚀 Quick Start

### Basic Usage
```python
from deepagents import DeepAgentsGraph
from deepagents.model_bedrock import BedrockModel

# Initialize with Bedrock
model = BedrockModel(model_id="anthropic.claude-3-haiku-20240307-v1:0")
graph = DeepAgentsGraph(model=model)

# Run analysis
result = graph.run("Analyze the sales data in data/sales.csv")
print(result)
```

### Advanced Usage with Custom Tools
```python
from deepagents import DeepAgentsGraph, CustomTool
from deepagents.model_bedrock import BedrockModel

# Create custom tool
def custom_analysis(data):
    # Your custom logic here
    return analysis_result

# Initialize with custom tools
model = BedrockModel(model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0")
graph = DeepAgentsGraph(
    model=model,
    custom_tools=[custom_analysis]
)

# Run with specific instructions
result = graph.run(
    query="Perform advanced analysis on the dataset",
    context={"dataset_path": "data/complex_data.csv"}
)
```

## 🤖 Supported Models

### Amazon Bedrock Models
- **Claude 3/3.5**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Claude 3.5 (Inference Profiles)**: `us.anthropic.claude-3-5-haiku-20241022-v1:0`
- **Titan**: `amazon.titan-text-express-v1`
- **Nova**: `amazon.nova-pro-v1:0`

### Model Configuration
```python
# Using inference profiles (recommended for Claude 3.5)
model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    region="us-east-1"
)

# With prompt caching (Claude models)
model = BedrockModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    enable_caching=True
)
```

## 🔧 Configuration

### Environment Variables
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Model Configuration
DEFAULT_MODEL_ID=us.anthropic.claude-3-5-haiku-20241022-v1:0
ENABLE_PROMPT_CACHING=true
MAX_TOKENS=4000
TEMPERATURE=0.7
```

### Bedrock Credentials (bedrock.json)
```json
{
    "aws_access_key_id": "your_access_key",
    "aws_secret_access_key": "your_secret_key",
    "aws_session_token": "optional_session_token"
}
```

## 🧪 Testing

Run the test suite to verify your setup:

```bash
# Test basic functionality
python test_deepagents_tools.py

# Test Bedrock integration
python test_bedrock_setup.py

# Test specific models
python test_bedrock_models.py

# Test prompt caching
python test_prompt_caching.py
```

## 📊 Examples

### Data Analysis
```python
# Analyze CSV data
result = graph.run("Analyze trends in sales_data.csv and create visualizations")

# Generate insights
result = graph.run("What are the key insights from the customer behavior data?")
```

### Code Generation
```python
# Generate Python code
result = graph.run("Create a machine learning model to predict customer churn")

# Code review and optimization
result = graph.run("Review and optimize the following Python code: [code]")
```

### Multi-step Analysis
```python
# Complex workflow
result = graph.run("""
1. Load and clean the dataset
2. Perform exploratory data analysis
3. Create predictive models
4. Generate a comprehensive report
""")
```

## 🔍 Troubleshooting

### Common Issues

1. **Model Access Errors**
   - Ensure you have access to the specific Bedrock models
   - Use inference profiles for Claude 3.5 models
   - Check AWS permissions

2. **Credential Issues**
   - Verify AWS credentials are properly configured
   - Use `aws sts get-caller-identity` to test
   - Check bedrock.json format

3. **Performance Issues**
   - Enable prompt caching for repeated queries
   - Use appropriate model sizes for your use case
   - Monitor token usage

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug information
result = graph.run(query, debug=True)
```

## 📚 Documentation

- **[Bedrock Integration Guide](BEDROCK_JSON_INTEGRATION.md)** - Complete setup guide
- **[Claude 3.5 Fix](CLAUDE_35_FIX.md)** - Inference profile configuration
- **[Prompt Caching Setup](PROMPT_CACHING_SETUP.md)** - Performance optimization
- **[API Reference](docs/api.md)** - Detailed API documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the docs/ directory for detailed guides
- **Examples**: See examples/ directory for usage patterns

## 🔄 Version History

- **v1.0.0**: Initial release with basic agent functionality
- **v1.1.0**: Added Amazon Bedrock integration
- **v1.2.0**: Claude 3.5 support with inference profiles
- **v1.3.0**: Prompt caching and performance optimizations
