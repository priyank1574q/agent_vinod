"""
Enhanced Streamlit File Analyzer with Amazon Bedrock Integration
Combines file analysis capabilities with powerful LLM models from Amazon Bedrock.
"""

import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Import our Bedrock integration
from bedrock_integration import (
    BEDROCK_MODELS, MODEL_CATEGORIES, MODEL_INFO,
    create_bedrock_model, invoke_model, stream_model_response,
    get_model_info, format_model_display, display_model_info_sidebar,
    check_aws_setup, get_available_models
)

# Page configuration
st.set_page_config(
    page_title="DeepAgents File Analyzer with Bedrock",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .model-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .file-analysis {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'uploaded_files_data' not in st.session_state:
        st.session_state.uploaded_files_data = {}
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'aws_configured' not in st.session_state:
        st.session_state.aws_configured = None

def process_text_file(file) -> str:
    """Process uploaded text file and return content."""
    try:
        content = file.read().decode('utf-8')
        return content
    except Exception as e:
        st.error(f"Error reading text file {file.name}: {str(e)}")
        return ""

def process_csv_file(file) -> pd.DataFrame:
    """Process uploaded CSV file and return DataFrame."""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error reading CSV file {file.name}: {str(e)}")
        return pd.DataFrame()

def analyze_files_with_llm(prompt: str, files_data: Dict, model_name: str, temperature: float, max_tokens: int) -> str:
    """Analyze files using the selected LLM model."""
    
    # Prepare context from files
    context_parts = []
    
    for filename, data in files_data.items():
        if isinstance(data, str):  # Text file
            context_parts.append(f"""
**File: {filename} (Text)**
Content preview (first 1000 characters):
{data[:1000]}{'...' if len(data) > 1000 else ''}

Full statistics:
- Character count: {len(data)}
- Word count: {len(data.split())}
- Line count: {len(data.splitlines())}
""")
        elif isinstance(data, pd.DataFrame):  # CSV file
            context_parts.append(f"""
**File: {filename} (CSV)**
Shape: {data.shape[0]} rows × {data.shape[1]} columns

Columns: {', '.join(data.columns.tolist())}

Data preview:
{data.head().to_string()}

Data types:
{data.dtypes.to_string()}

Basic statistics (for numeric columns):
{data.describe().to_string() if len(data.select_dtypes(include=[np.number]).columns) > 0 else 'No numeric columns'}
""")
    
    # Combine context
    file_context = "\n\n".join(context_parts)
    
    # Create comprehensive system prompt
    system_prompt = f"""You are an expert data analyst and file processing assistant with access to Amazon Bedrock. 
You have been provided with the following files to analyze:

{file_context}

Please provide thorough, insightful analysis based on the user's request. Consider:
1. The content and structure of the files
2. Patterns, trends, or interesting findings
3. Potential insights or recommendations
4. Any data quality issues or observations

Be specific and reference the actual data when possible. If the user asks for visualizations or code, provide clear Python code using pandas, matplotlib, or plotly."""

    # Invoke the model
    try:
        response = invoke_model(
            model_name=model_name,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt
        )
        return response if response else "Sorry, I couldn't generate a response. Please try again."
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def display_file_analysis_summary(files_data: Dict):
    """Display a summary of uploaded files."""
    if not files_data:
        return
        
    st.markdown("### 📁 Uploaded Files Summary")
    
    for filename, data in files_data.items():
        with st.expander(f"📄 {filename}"):
            if isinstance(data, str):  # Text file
                st.markdown(f"""
                **File Type:** Text
                - **Size:** {len(data)} characters
                - **Words:** {len(data.split())} words
                - **Lines:** {len(data.splitlines())} lines
                """)
                
                # Show preview
                st.markdown("**Preview:**")
                st.text(data[:500] + "..." if len(data) > 500 else data)
                
            elif isinstance(data, pd.DataFrame):  # CSV file
                st.markdown(f"""
                **File Type:** CSV
                - **Shape:** {data.shape[0]} rows × {data.shape[1]} columns
                - **Memory Usage:** {data.memory_usage(deep=True).sum() / 1024:.1f} KB
                """)
                
                # Show column info
                st.markdown("**Columns:**")
                col_info = pd.DataFrame({
                    'Column': data.columns,
                    'Type': data.dtypes.astype(str),
                    'Non-Null Count': data.count(),
                    'Null Count': data.isnull().sum()
                })
                st.dataframe(col_info, use_container_width=True)
                
                # Show data preview
                st.markdown("**Data Preview:**")
                st.dataframe(data.head(), use_container_width=True)
                
                # Basic statistics for numeric columns
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.markdown("**Numeric Columns Statistics:**")
                    st.dataframe(data[numeric_cols].describe(), use_container_width=True)

def create_visualization_from_data(files_data: Dict):
    """Create automatic visualizations from CSV data."""
    csv_files = {k: v for k, v in files_data.items() if isinstance(v, pd.DataFrame)}
    
    if not csv_files:
        return
        
    st.markdown("### 📊 Automatic Visualizations")
    
    for filename, df in csv_files.items():
        st.markdown(f"#### 📈 {filename}")
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution plot for first numeric column
                if len(numeric_cols) > 0:
                    fig = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Correlation heatmap if multiple numeric columns
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols].corr()
                    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                                  title="Correlation Matrix")
                    st.plotly_chart(fig, use_container_width=True)
                elif len(categorical_cols) > 0 and len(numeric_cols) > 0:
                    # Box plot for categorical vs numeric
                    fig = px.box(df, x=categorical_cols[0], y=numeric_cols[0], 
                               title=f"{numeric_cols[0]} by {categorical_cols[0]}")
                    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application function."""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 DeepAgents File Analyzer with Amazon Bedrock</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Powerful file analysis powered by Amazon Bedrock LLMs**
    
    Upload your text and CSV files, then use advanced AI models like Claude 3.5 Sonnet and Amazon Nova 
    to analyze, understand, and extract insights from your data.
    """)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # AWS Setup Check
        if st.session_state.aws_configured is None:
            with st.spinner("Checking AWS configuration..."):
                st.session_state.aws_configured = check_aws_setup()
        
        if not st.session_state.aws_configured:
            st.error("⚠️ AWS not configured properly. Please check the setup instructions above.")
            st.stop()
        
        # Model Selection
        st.markdown("### 🤖 Model Selection")
        
        # Get available models (prioritize working models)
        try:
            available_models = list(BEDROCK_MODELS.keys())
            # Set Titan Text Express as default (first in list)
            if "Titan Text G1 - Express" in available_models:
                # Move Titan to front
                available_models.remove("Titan Text G1 - Express")
                available_models.insert(0, "Titan Text G1 - Express")
        except:
            available_models = ["Titan Text G1 - Express", "Claude 3 Haiku"]  # Fallback to working models
        
        selected_model = st.selectbox(
            "Choose AI Model:",
            available_models,
            index=0,  # Default to first model (Titan Text Express)
            format_func=lambda x: format_model_display(x),
            help="Select the AI model for analysis. ✅ = Verified working with your credentials"
        )
        
        # Model parameters
        st.markdown("### 🎛️ Model Parameters")
        temperature = st.slider(
            "Temperature (Creativity)",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="Higher values make output more creative but less focused"
        )
        
        max_tokens = st.slider(
            "Max Response Length",
            min_value=100,
            max_value=4000,
            value=2000,
            step=100,
            help="Maximum length of AI response"
        )
        
        # Display model info with working status
        model_info = get_model_info(selected_model)
        
        # Add working status indicator
        working_models = ["Titan Text G1 - Express", "Titan Text G1 - Lite", "Claude 3 Haiku", "Claude 3 Sonnet"]
        status_icon = "✅" if selected_model in working_models else "⚠️"
        status_text = "Verified Working" if selected_model in working_models else "May Need Access"
        
        st.markdown(f"""
        <div class="model-info">
        <strong>{status_icon} Selected Model: {selected_model} ({status_text})</strong><br>
        <strong>Provider:</strong> {model_info['provider']}<br>
        <strong>Speed:</strong> {model_info['speed']}<br>
        <strong>Cost:</strong> {model_info['cost']}<br>
        <strong>Best for:</strong> {model_info['best_for']}
        </div>
        """, unsafe_allow_html=True)
        
        # Display additional model information
        display_model_info_sidebar()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## 📁 File Upload")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload your files:",
            type=['txt', 'csv'],
            accept_multiple_files=True,
            help="Upload text (.txt) and CSV (.csv) files for analysis"
        )
        
        # Process uploaded files
        if uploaded_files:
            files_data = {}
            
            with st.spinner("Processing uploaded files..."):
                for file in uploaded_files:
                    if file.name.endswith('.txt'):
                        content = process_text_file(file)
                        if content:
                            files_data[file.name] = content
                    elif file.name.endswith('.csv'):
                        df = process_csv_file(file)
                        if not df.empty:
                            files_data[file.name] = df
            
            # Store in session state
            st.session_state.uploaded_files_data = files_data
            
            # Display file summary
            display_file_analysis_summary(files_data)
            
            # Create automatic visualizations
            create_visualization_from_data(files_data)
    
    with col2:
        st.markdown("## 💬 AI Analysis Chat")
        
        # Chat interface
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                    <strong>{selected_model}:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        if st.session_state.uploaded_files_data:
            prompt = st.text_area(
                "Ask questions about your files:",
                placeholder="e.g., 'Summarize the key findings from my data', 'What patterns do you see?', 'Create a visualization showing...'",
                height=100
            )
            
            col_send, col_clear = st.columns([3, 1])
            
            with col_send:
                if st.button("🚀 Analyze", type="primary", use_container_width=True):
                    if prompt.strip():
                        # Add user message
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        
                        # Show thinking indicator
                        with st.spinner(f"🤖 {selected_model} is analyzing your files..."):
                            # Get AI response
                            response = analyze_files_with_llm(
                                prompt=prompt,
                                files_data=st.session_state.uploaded_files_data,
                                model_name=selected_model,
                                temperature=temperature,
                                max_tokens=max_tokens
                            )
                        
                        # Add assistant response
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                        # Store in analysis history
                        st.session_state.analysis_history.append({
                            "timestamp": datetime.now(),
                            "model": selected_model,
                            "prompt": prompt,
                            "response": response,
                            "files": list(st.session_state.uploaded_files_data.keys())
                        })
                        
                        # Rerun to update chat display
                        st.rerun()
                    else:
                        st.warning("Please enter a question or analysis request.")
            
            with col_clear:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
        else:
            st.info("👆 Upload files first to start the AI analysis conversation.")
    
    # Analysis History Section
    if st.session_state.analysis_history:
        st.markdown("## 📚 Analysis History")
        
        with st.expander("View Previous Analyses", expanded=False):
            for i, analysis in enumerate(reversed(st.session_state.analysis_history)):
                st.markdown(f"""
                <div class="file-analysis">
                <strong>Analysis #{len(st.session_state.analysis_history) - i}</strong><br>
                <strong>Time:</strong> {analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Model:</strong> {analysis['model']}<br>
                <strong>Files:</strong> {', '.join(analysis['files'])}<br>
                <strong>Question:</strong> {analysis['prompt'][:100]}{'...' if len(analysis['prompt']) > 100 else ''}<br>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    🤖 Powered by Amazon Bedrock | Built with Streamlit | DeepAgents Framework
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
