#!/usr/bin/env python3
"""
Example Streamlit app that uses bedrock.json for Bedrock credentials
"""

import streamlit as st
import json
from bedrock_credentials_handler import BedrockCredentialsHandler
from botocore.exceptions import ClientError

# Initialize session state
if 'bedrock_handler' not in st.session_state:
    st.session_state.bedrock_handler = None
if 'bedrock_client' not in st.session_state:
    st.session_state.bedrock_client = None

def initialize_bedrock():
    """Initialize Bedrock client using bedrock.json credentials"""
    try:
        handler = BedrockCredentialsHandler()
        
        # Load credentials
        if handler.load_bedrock_credentials():
            client = handler.create_bedrock_client()
            st.session_state.bedrock_handler = handler
            st.session_state.bedrock_client = client
            return True, "✅ Bedrock initialized successfully"
        else:
            return False, "❌ Failed to load credentials from bedrock.json"
            
    except Exception as e:
        return False, f"❌ Error initializing Bedrock: {str(e)}"

def call_bedrock_model(prompt, model_id="amazon.titan-text-express-v1", max_tokens=100):
    """Call a Bedrock model with the given prompt"""
    if not st.session_state.bedrock_client:
        return None, "Bedrock client not initialized"
    
    try:
        # Prepare request body based on model type
        if "titan" in model_id.lower():
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }
        elif "claude" in model_id.lower():
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
        elif "ai21" in model_id.lower():
            body = {
                "prompt": prompt,
                "maxTokens": max_tokens,
                "temperature": 0.7
            }
        else:
            # Default to Titan format
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": 0.7
                }
            }
        
        # Make the API call
        response = st.session_state.bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        # Parse response based on model type
        response_body = json.loads(response['body'].read())
        
        if "titan" in model_id.lower():
            text = response_body.get('results', [{}])[0].get('outputText', '')
        elif "claude" in model_id.lower():
            text = response_body.get('content', [{}])[0].get('text', '')
        elif "ai21" in model_id.lower():
            text = response_body.get('completions', [{}])[0].get('data', {}).get('text', '')
        else:
            text = str(response_body)
        
        return text, None
        
    except ClientError as e:
        error_msg = f"AWS Error: {e.response['Error']['Code']} - {e.response['Error']['Message']}"
        return None, error_msg
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    st.title("🤖 Bedrock Chat with bedrock.json Credentials")
    st.markdown("This app uses credentials from `bedrock.json` to access AWS Bedrock models.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Initialize Bedrock button
        if st.button("🔐 Initialize Bedrock"):
            with st.spinner("Loading credentials from bedrock.json..."):
                success, message = initialize_bedrock()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        # Show connection status
        if st.session_state.bedrock_client:
            st.success("🟢 Bedrock Connected")
        else:
            st.warning("🟡 Bedrock Not Connected")
        
        # Model selection
        model_options = {
            "Titan Text Express": "amazon.titan-text-express-v1",
            "Titan Text Lite": "amazon.titan-text-lite-v1",
            "Claude 3 Haiku": "anthropic.claude-3-haiku-20240307-v1:0",
            "Claude 3 Sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
            "Claude 3.5 Haiku": "us.anthropic.claude-3-5-haiku-20241022-v1:0",
            "Claude 3.5 Sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        }
        
        selected_model_name = st.selectbox(
            "🤖 Select Model",
            options=list(model_options.keys()),
            index=0
        )
        selected_model_id = model_options[selected_model_name]
        
        # Parameters
        max_tokens = st.slider("📝 Max Tokens", min_value=10, max_value=500, value=100)
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Check if Bedrock is initialized
    if not st.session_state.bedrock_client:
        st.info("👆 Please initialize Bedrock using the sidebar first.")
        st.code("""
# Your bedrock.json should contain credentials in one of these formats:

# Format 1: Direct AWS credentials
{
    "aws_access_key_id": "YOUR_ACCESS_KEY",
    "aws_secret_access_key": "YOUR_SECRET_KEY",
    "aws_session_token": "YOUR_SESSION_TOKEN"  // Optional for temporary credentials
}

# Format 2: Base64 encoded credentials or API key
"base64_encoded_credentials_or_api_key"
        """)
        return
    
    # Chat input
    user_prompt = st.text_area(
        "💭 Enter your prompt:",
        placeholder="Ask me anything...",
        height=100
    )
    
    # Generate response
    if st.button("🚀 Generate Response", disabled=not user_prompt.strip()):
        if user_prompt.strip():
            with st.spinner(f"Generating response using {selected_model_name}..."):
                response_text, error = call_bedrock_model(
                    user_prompt, 
                    selected_model_id, 
                    max_tokens
                )
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.success("✅ Response generated successfully!")
                    st.markdown("### 🤖 AI Response:")
                    st.markdown(response_text)
    
    # Example prompts
    st.header("💡 Example Prompts")
    example_prompts = [
        "What is AWS Bedrock and how does it work?",
        "Explain the benefits of using AI in cloud computing.",
        "Write a Python function to calculate fibonacci numbers.",
        "What are the best practices for AWS security?",
        "Explain machine learning in simple terms."
    ]
    
    for i, prompt in enumerate(example_prompts):
        if st.button(f"📝 {prompt}", key=f"example_{i}"):
            st.text_area("💭 Enter your prompt:", value=prompt, height=100, key=f"prompt_area_{i}")

if __name__ == "__main__":
    main()
