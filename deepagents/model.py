from langchain_openai import AzureChatOpenAI
# from lib.genai_init import *
# import vertexai
# from langchain_google_vertexai import ChatVertexAI


def get_default_model(loaded_creds,temperature=0.0,max_tokens=512):
    chat_gpt_model_4o = AzureChatOpenAI(
    azure_endpoint=loaded_creds["azure_endpoint"],
    openai_api_version=loaded_creds["openai_api_version"],
    deployment_name=loaded_creds["deployment_name"],
    openai_api_key=loaded_creds["openai_api_key"],
    openai_api_type=loaded_creds["openai_api_type"],
    temperature=0.0,
    max_tokens=2048
)
    return chat_gpt_model_4o



# def get_gemini(temperature=0.0,max_tokens=512):
#     vertexai.init(project=PROJECT_ID, location="us-central1",credentials=credentials)
#     llm = ChatVertexAI(
#   project=PROJECT_ID, model_name="gemini-2.0-flash-001" ,# "gemini-1.5-flash-001"
#   location="us-central1", credentials=credentials, max_output_tokens=256,
#   temperature=0, top_p=1, timeout=120, max_retries=4
# )
#     return llm
