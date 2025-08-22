# Claude 3.5 Model Fix - Inference Profiles

## 🐛 Problem
You were getting this error when trying to use Claude 3.5 models:
```
Model invocation failed: An error occurred (ValidationException) when calling the InvokeModel operation: 
Invocation of model ID anthropic.claude-3-5-haiku-20241022-v1:0 with on-demand throughput isn't supported. 
Retry your request with the ID or ARN of an inference profile that contains this model.
```

## 🔧 Root Cause
Claude 3.5 models require **inference profiles** instead of direct model IDs for on-demand access. The direct model IDs only work with provisioned throughput.

## ✅ Solution
Updated the model IDs to use the correct US inference profiles:

### Before (❌ Broken)
```python
"Claude 3.5 Haiku": "anthropic.claude-3-5-haiku-20241022-v1:0"
"Claude 3.5 Sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0"
```

### After (✅ Fixed)
```python
"Claude 3.5 Haiku": "us.anthropic.claude-3-5-haiku-20241022-v1:0"
"Claude 3.5 Sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
```

## 🧪 Test Results
✅ **Claude 3.5 Haiku (US Profile)**: Working correctly
✅ **Claude 3.5 Sonnet (US Profile)**: Working correctly
❌ **Claude 3 Opus (US Profile)**: Access denied (requires special access)

## 📁 Files Updated
1. **`bedrock_integration.py`** - Updated model IDs and categories
2. **`test_bedrock_with_json.py`** - Updated test models
3. **`test_fixed_models.py`** - New test script to verify fixes

## 🌍 Available Inference Profiles
- **US Region**: `us.anthropic.claude-3-5-haiku-20241022-v1:0`
- **EU Region**: `eu.anthropic.claude-3-5-haiku-20241022-v1:0`
- **Cross-Region**: Available for load balancing

## 🚀 Status
- ✅ **Streamlit app restarted** with fixed model IDs
- ✅ **Claude 3.5 models now working** in the deepagents-streamlit app
- ✅ **All existing functionality preserved**

## 💡 Key Learnings
1. **Inference Profiles** are required for newer Claude models with on-demand throughput
2. **Regional prefixes** (us., eu.) indicate the inference profile region
3. **Legacy Claude models** (3.0) still work with direct model IDs
4. **Always test model IDs** before deploying to production

## 🎯 Next Steps
You can now use Claude 3.5 Haiku and Sonnet models in your Streamlit app without errors. The models will appear in the "Anthropic Claude (✅ Working)" category in the model selector.
