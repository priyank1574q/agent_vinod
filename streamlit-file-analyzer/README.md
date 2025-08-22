# Streamlit File Analyzer with Amazon Bedrock

An interactive web application for file analysis and AI-powered insights using Amazon Bedrock models.

## 🚀 Features

- **File Upload & Analysis**: Support for CSV, JSON, TXT, and other file formats
- **AI-Powered Insights**: Generate insights using Amazon Bedrock models
- **Interactive Chat**: Chat with AI about your uploaded files
- **Data Visualization**: Create charts and graphs from your data
- **Multiple AI Models**: Choose from Claude, Titan, and other Bedrock models
- **Real-time Processing**: Stream responses for better user experience

## 📁 Project Structure

```
streamlit-file-analyzer/
├── app_bedrock.py              # Main Streamlit application
├── bedrock_integration.py      # Bedrock model integration
├── bedrock_credentials_handler.py # Credential management
├── requirements.txt            # Python dependencies
├── start_app.sh               # Application startup script
├── sample_data/               # Sample datasets for testing
│   ├── sales_data.csv
│   └── analysis_report.txt
├── examples/
│   ├── streamlit_app.py       # Basic Streamlit example
│   └── streamlit_bedrock_example.py # Bedrock integration example
├── credentials/
│   ├── aws_credentials_template.json # AWS credentials template
│   ├── load_aws_credentials.py       # Credential loading utilities
│   └── export_aws_creds.sh          # Credential export script
├── tests/
│   ├── test_integration.py    # Integration tests
│   └── dry_test.py           # Dry run tests
└── logs/                     # Application logs
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd streamlit-file-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up AWS credentials**

   **Option 1: AWS CLI**
   ```bash
   aws configure
   ```

   **Option 2: Environment variables**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

   **Option 3: bedrock.json file**
   ```json
   {
       "aws_access_key_id": "your_access_key",
       "aws_secret_access_key": "your_secret_key",
       "aws_session_token": "optional_session_token"
   }
   ```

## 🚀 Quick Start

### Using the Startup Script (Recommended)
```bash
chmod +x start_app.sh
./start_app.sh
```

### Manual Start
```bash
streamlit run app_bedrock.py --server.port=8501 --server.address=0.0.0.0
```

### Access the Application
- **Local**: http://localhost:8501
- **External**: http://your-server-ip:8501

## 🤖 Supported AI Models

### Amazon Bedrock Models

#### ✅ Working Models
- **Amazon Titan Text Express**: `amazon.titan-text-express-v1`
- **Amazon Titan Text Lite**: `amazon.titan-text-lite-v1`
- **Claude 3 Haiku**: `anthropic.claude-3-haiku-20240307-v1:0`
- **Claude 3 Sonnet**: `anthropic.claude-3-sonnet-20240229-v1:0`

#### ✅ Claude 3.5 Models (Inference Profiles)
- **Claude 3.5 Haiku**: `us.anthropic.claude-3-5-haiku-20241022-v1:0`
- **Claude 3.5 Sonnet**: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`

#### ⚠️ Models Requiring Special Access
- **Claude 3 Opus**: `us.anthropic.claude-3-opus-20240229-v1:0`
- **Amazon Nova Models**: `amazon.nova-pro-v1:0`
- **Meta Llama Models**: `meta.llama3-2-90b-instruct-v1:0`

## 📊 Application Features

### File Analysis
- **Upload Files**: Drag and drop or browse to upload files
- **Automatic Detection**: Automatically detects file type and structure
- **Data Preview**: View file contents and basic statistics
- **Format Support**: CSV, JSON, TXT, Excel, and more

### AI-Powered Analysis
- **Generate Insights**: Ask AI to analyze your data
- **Custom Queries**: Ask specific questions about your files
- **Multiple Models**: Switch between different AI models
- **Streaming Responses**: Real-time response generation

### Data Visualization
- **Interactive Charts**: Create charts using Plotly
- **Statistical Analysis**: Generate descriptive statistics
- **Custom Visualizations**: AI-generated visualization code
- **Export Options**: Download charts and analysis results

### Chat Interface
- **Conversational AI**: Natural language interaction
- **Context Awareness**: AI remembers previous conversations
- **File Context**: AI understands your uploaded files
- **Multi-turn Conversations**: Extended discussions about data

## 🔧 Configuration

### Model Configuration
```python
# In bedrock_integration.py
BEDROCK_MODELS = {
    "Titan Text Express": "amazon.titan-text-express-v1",
    "Claude 3.5 Haiku": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    # Add more models as needed
}
```

### Application Settings
```python
# Streamlit configuration
st.set_page_config(
    page_title="File Analyzer with Bedrock",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### AWS Credentials
The application supports multiple credential methods:

1. **bedrock.json** (Recommended)
2. **Environment variables**
3. **AWS CLI configuration**
4. **IAM roles** (for EC2 instances)

## 🧪 Testing

### Run Integration Tests
```bash
python test_integration.py
```

### Test Bedrock Connection
```python
from bedrock_credentials_handler import BedrockCredentialsHandler

handler = BedrockCredentialsHandler()
client = handler.create_bedrock_client()
# Test successful if no errors
```

### Dry Run Test
```bash
python dry_test.py
```

## 📱 Usage Examples

### Basic File Analysis
1. Start the application
2. Upload a CSV file
3. Select an AI model (e.g., "Claude 3.5 Haiku")
4. Ask: "What are the key insights from this data?"
5. View the AI-generated analysis

### Advanced Data Analysis
1. Upload multiple related files
2. Use the chat interface to ask complex questions
3. Request specific visualizations
4. Export results and charts

### Custom Analysis Workflows
```python
# Example: Custom analysis prompt
prompt = """
Analyze this sales data and provide:
1. Revenue trends over time
2. Top performing products
3. Customer segmentation insights
4. Recommendations for improvement
"""
```

## 🔍 Troubleshooting

### Common Issues

1. **Model Access Errors**
   ```
   Error: You don't have access to the model
   ```
   **Solution**: Request access to the model in AWS Console or use available models

2. **Credential Issues**
   ```
   Error: Unable to locate credentials
   ```
   **Solution**: Check AWS credentials configuration

3. **Port Already in Use**
   ```
   Error: Port 8501 is already in use
   ```
   **Solution**: 
   ```bash
   lsof -i :8501  # Find process using port
   kill <process_id>  # Kill the process
   ```

4. **Claude 3.5 Validation Error**
   ```
   Error: Invocation of model ID ... with on-demand throughput isn't supported
   ```
   **Solution**: Use inference profile IDs (us.anthropic.claude-3-5-haiku-20241022-v1:0)

### Debug Mode
Enable debug logging in the application:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app_bedrock.py
```

### Production Deployment
```bash
# Using the startup script
nohup ./start_app.sh > app.log 2>&1 &

# Or with custom configuration
streamlit run app_bedrock.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app_bedrock.py", "--server.address=0.0.0.0"]
```

## 🔒 Security Considerations

- **Credentials**: Never commit AWS credentials to version control
- **File Uploads**: Validate file types and sizes
- **API Keys**: Use environment variables or secure credential storage
- **Network**: Use HTTPS in production
- **Access Control**: Implement authentication if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include tests for new features
- Update documentation

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check the README and code comments
- **Examples**: See the examples/ directory

## 🔄 Version History

- **v1.0.0**: Initial Streamlit application
- **v1.1.0**: Added Amazon Bedrock integration
- **v1.2.0**: Fixed Claude 3.5 model support
- **v1.3.0**: Enhanced file analysis capabilities
- **v1.4.0**: Added chat interface and streaming responses

## 🌟 Features Roadmap

- [ ] Support for more file formats
- [ ] Advanced visualization options
- [ ] User authentication
- [ ] Data export capabilities
- [ ] Batch processing
- [ ] API endpoints
- [ ] Mobile-responsive design
