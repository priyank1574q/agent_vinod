# Bedrock.json Integration Guide

This guide shows how to incorporate your `bedrock.json` file for AWS Bedrock credentials in your Python applications.

## 📁 Files Created

1. **`bedrock_credentials_handler.py`** - Main handler class for bedrock.json credentials
2. **`test_bedrock_with_json.py`** - Test script to check available models
3. **`streamlit_bedrock_example.py`** - Example Streamlit app using bedrock.json
4. **`bedrock_integration_guide.py`** - Comprehensive integration examples

## 🚀 Quick Start

### Method 1: Direct Integration (Recommended)

```python
from bedrock_credentials_handler import BedrockCredentialsHandler
import json

# Initialize handler
handler = BedrockCredentialsHandler()

# Create Bedrock client
bedrock_client = handler.create_bedrock_client()

# Use the client
body = {
    "inputText": "Your prompt here",
    "textGenerationConfig": {
        "maxTokenCount": 100,
        "temperature": 0.7
    }
}

response = bedrock_client.invoke_model(
    modelId="amazon.titan-text-express-v1",
    body=json.dumps(body),
    contentType='application/json'
)
```

### Method 2: Environment Variables

```python
from bedrock_credentials_handler import BedrockCredentialsHandler
import boto3

# Set environment variables from bedrock.json
handler = BedrockCredentialsHandler()
handler.set_environment_variables()

# Use standard boto3
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
```

### Method 3: One-line Function

```python
def create_bedrock_client_from_json():
    handler = BedrockCredentialsHandler()
    return handler.create_bedrock_client()

# Use it
client = create_bedrock_client_from_json()
```

## 🎯 Available Models

Your bedrock.json credentials provide access to these models:

✅ **Available Models:**
- `amazon.titan-text-express-v1` (Recommended)
- `amazon.titan-text-lite-v1`
- `anthropic.claude-3-haiku-20240307-v1:0`
- `anthropic.claude-3-sonnet-20240229-v1:0`
- `us.anthropic.claude-3-5-haiku-20241022-v1:0`
- `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

❌ **Unavailable Models:**
- AI21 Jurassic models (Access denied)
- Amazon Nova models (Different API format)

## 🧪 Testing Your Setup

Run the test script to verify everything works:

```bash
python3 test_bedrock_with_json.py
```

## 📱 Streamlit Integration

For Streamlit apps, use the example:

```bash
streamlit run streamlit_bedrock_example.py
```

## 🔧 Integration Examples

### For Existing Code

If you have existing code that uses hardcoded credentials, replace:

```python
# OLD WAY
os.environ['AWS_ACCESS_KEY_ID'] = 'hardcoded_key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'hardcoded_secret'
bedrock = boto3.client('bedrock-runtime')
```

With:

```python
# NEW WAY
from bedrock_credentials_handler import BedrockCredentialsHandler
handler = BedrockCredentialsHandler()
bedrock = handler.create_bedrock_client()
```

### For Class-based Applications

```python
class MyApp:
    def __init__(self):
        self.handler = BedrockCredentialsHandler()
        self.bedrock = self.handler.create_bedrock_client()
    
    def generate_text(self, prompt):
        # Use self.bedrock for API calls
        pass
```

## 🛠️ Model-Specific Request Formats

### Titan Models
```python
body = {
    "inputText": "Your prompt",
    "textGenerationConfig": {
        "maxTokenCount": 100,
        "temperature": 0.7
    }
}
```

### Claude Models
```python
body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Your prompt"}],
    "temperature": 0.7
}
```

## 🔒 Security Notes

- The `bedrock.json` file contains sensitive credentials
- Keep it secure and don't commit it to version control
- The handler automatically detects the credential format
- Supports both direct credentials and encoded formats

## 🐛 Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Ensure `bedrock.json` exists in `/home/ec2-user/`
   - Check file permissions

2. **"Access denied" errors**
   - Verify your AWS account has Bedrock access
   - Check if specific models need to be enabled

3. **"Invalid JSON" errors**
   - The handler supports multiple formats
   - Base64 encoded content is automatically decoded

### Debug Commands

```bash
# Test credentials loading
python3 bedrock_credentials_handler.py

# Test all available models
python3 test_bedrock_with_json.py

# See all integration methods
python3 bedrock_integration_guide.py
```

## 📚 Next Steps

1. **Choose your integration method** based on your application type
2. **Test with available models** to find the best one for your use case
3. **Update your existing code** to use bedrock.json credentials
4. **Consider using Claude 3.5 models** for advanced capabilities

## 💡 Best Practices

- Use `amazon.titan-text-express-v1` for general text generation
- Use Claude models for complex reasoning and analysis
- Set appropriate `maxTokenCount` to control response length
- Use temperature 0.1-0.3 for factual responses, 0.7-0.9 for creative content
- Handle API errors gracefully in production code

---

Your bedrock.json integration is now complete and ready to use! 🎉
