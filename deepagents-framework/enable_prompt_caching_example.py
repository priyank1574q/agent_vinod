"""
Example of how to enable prompt caching for Bedrock models
"""

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

def get_claude_with_caching(
    model_name: str = "claude-3-5-sonnet",
    temperature: float = 0.0,
    max_tokens: int = 4096,
    region_name: str = "us-east-1",
    **kwargs
) -> ChatBedrock:
    """
    Initialize Claude model with prompt caching enabled.
    """
    model_id = f"anthropic.{model_name}-20241022-v2:0"
    
    # Enable prompt caching in model kwargs
    model_kwargs = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        # Enable prompt caching
        "extra_body": {
            "cache_control": {"type": "ephemeral"}
        },
        **kwargs
    }
    
    return ChatBedrock(
        model_id=model_id,
        model_kwargs=model_kwargs,
        region_name=region_name,
    )

def create_cacheable_messages(system_prompt: str, user_message: str):
    """
    Create messages with cache control markers.
    """
    return [
        SystemMessage(
            content=system_prompt,
            # Mark system message for caching
            additional_kwargs={
                "cache_control": {"type": "ephemeral"}
            }
        ),
        HumanMessage(content=user_message)
    ]

# Example usage
if __name__ == "__main__":
    # Initialize model with caching
    model = get_claude_with_caching()
    
    # Create cacheable system prompt
    system_prompt = """You are an expert software developer assistant. 
    You help with code review, debugging, and optimization.
    Always provide detailed explanations and follow best practices."""
    
    # Create messages with cache markers
    messages = create_cacheable_messages(
        system_prompt=system_prompt,
        user_message="How can I optimize this Python function?"
    )
    
    # First call - will cache the system prompt
    response1 = model.invoke(messages)
    print("First response:", response1.content[:100] + "...")
    
    # Subsequent calls will use cached system prompt
    messages2 = create_cacheable_messages(
        system_prompt=system_prompt,  # Same system prompt - will use cache
        user_message="What are Python best practices for error handling?"
    )
    
    response2 = model.invoke(messages2)
    print("Second response:", response2.content[:100] + "...")
