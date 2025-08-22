from deepagents.sub_agent import _create_task_tool, SubAgent
from deepagents.model import get_default_model, get_bedrock_model, get_anthropic_claude, get_amazon_nova
from deepagents.tools import write_todos, write_file, read_file, ls, edit_file
from deepagents.state import DeepAgentState
from typing import Sequence, Union, Callable, Any, TypeVar, Type, Optional, Dict
from langchain_core.tools import BaseTool
from langchain_core.language_models import LanguageModelLike
from deepagents.interrupt import create_interrupt_hook, ToolInterruptConfig
from langgraph.types import Checkpointer
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

StateSchema = TypeVar("StateSchema", bound=DeepAgentState)
StateSchemaType = Type[StateSchema]

base_prompt = """You have access to a number of standard tools

## `write_todos`

You have access to the `write_todos` tools to help you manage and plan tasks. Use these tools VERY frequently to ensure that you are tracking your tasks and giving the user visibility into your progress.
These tools are also EXTREMELY helpful for planning tasks, and for breaking down larger complex tasks into smaller steps. If you do not use this tool when planning, you may forget to do important tasks - and that is unacceptable.

It is critical that you mark todos as completed as soon as you are done with a task. Do not batch up multiple tasks before marking them as completed.
## `task`

- When doing web search, prefer to use the `task` tool in order to reduce context usage."""


def create_deep_agent(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]],
    instructions: str,
    model: Optional[Union[str, LanguageModelLike]] = None,
    subagents: list[SubAgent] = None,
    state_schema: Optional[StateSchemaType] = None,
    interrupt_config: Optional[ToolInterruptConfig] = None,
    config_schema: Optional[Type[Any]] = None,
    checkpointer: Optional[Checkpointer] = None,
    post_model_hook: Optional[Callable] = None,
    # New Bedrock-specific parameters
    loaded_creds: Optional[Dict[str, Any]] = None,
    use_bedrock: bool = False,
    bedrock_model_name: str = "claude-3-5-sonnet",
    temperature: float = 0.0,
    max_tokens: int = 4096,
):
    """Create a deep agent.

    This agent will by default have access to a tool to write todos (write_todos),
    and then four file editing tools: write_file, ls, read_file, edit_file.

    Args:
        tools: The additional tools the agent should have access to.
        instructions: The additional instructions the agent should have. Will go in
            the system prompt.
        model: The model to use. If None, will use get_default_model.
        subagents: The subagents to use. Each subagent should be a dictionary with the
            following keys:
                - `name`
                - `description` (used by the main agent to decide whether to call the sub agent)
                - `prompt` (used as the system prompt in the subagent)
                - (optional) `tools`
        state_schema: The schema of the deep agent. Should subclass from DeepAgentState
        interrupt_config: Optional Dict[str, HumanInterruptConfig] mapping tool names to interrupt configs.
        config_schema: The schema of the deep agent.
        checkpointer: Optional checkpointer for persisting agent state between runs.
        post_model_hook: Optional post-processing hook for model responses.
        
        # Bedrock-specific parameters
        loaded_creds: Azure OpenAI credentials (for backward compatibility)
        use_bedrock: Whether to use Amazon Bedrock models
        bedrock_model_name: Name of the Bedrock model to use
        temperature: Sampling temperature for the model
        max_tokens: Maximum tokens to generate
    """
    
    system_prompt = instructions + base_prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    
    built_in_tools = [write_todos, write_file, read_file, ls, edit_file]
    
    if model is None:
        if use_bedrock:
            model = get_bedrock_model(
                model_name=bedrock_model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            model = get_default_model(
                loaded_creds=loaded_creds,
                temperature=temperature,
                max_tokens=max_tokens
            )
    
    state_schema = state_schema or DeepAgentState
    task_tool = _create_task_tool(
        list(tools) + built_in_tools,
        instructions,
        subagents or [],
        model,
        state_schema
    )
    all_tools = built_in_tools + list(tools) + [task_tool]
    
    # Should never be the case that both are specified
    if post_model_hook and interrupt_config:
        raise ValueError(
            "Cannot specify both post_model_hook and interrupt_config together. "
            "Use either interrupt_config for tool interrupts or post_model_hook for custom post-processing."
        )
    elif post_model_hook is not None:
        selected_post_model_hook = post_model_hook
    elif interrupt_config is not None:
        selected_post_model_hook = create_interrupt_hook(interrupt_config)
    else:
        selected_post_model_hook = None
    
    return create_react_agent(
        model,
        prompt=prompt,
        tools=all_tools,
        state_schema=state_schema,
        post_model_hook=selected_post_model_hook,
        config_schema=config_schema,
        checkpointer=checkpointer,
    )

# Convenience functions for creating agents with specific Bedrock models
def create_claude_agent(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]],
    instructions: str,
    model_name: str = "claude-3-5-sonnet",
    temperature: float = 0.0,
    max_tokens: int = 4096,
    **kwargs
):
    """Create a deep agent using Anthropic Claude via Bedrock."""
    return create_deep_agent(
        tools=tools,
        instructions=instructions,
        use_bedrock=True,
        bedrock_model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )

def create_nova_agent(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]],
    instructions: str,
    model_name: str = "nova-pro",
    temperature: float = 0.0,
    max_tokens: int = 4096,
    **kwargs
):
    """Create a deep agent using Amazon Nova via Bedrock."""
    return create_deep_agent(
        tools=tools,
        instructions=instructions,
        use_bedrock=True,
        bedrock_model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )


