from langgraph.prebuilt.chat_agent_executor import AgentState
from typing import  Annotated
from typing import Literal
from typing_extensions import TypedDict,NotRequired


class Todo(TypedDict):
    """Todo to track."""

    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(l, r):
    if l is None:
        return r
    elif r is None:
        return l
    else:
        return {**l, **r}


class DeepAgentState(AgentState):
    todos: NotRequired[list[Todo]]
    files: Annotated[NotRequired[dict[str, str]], file_reducer]
    files_backup: NotRequired[dict[str, str]]
    python_namespace: NotRequired[dict]
    images: Annotated[NotRequired[dict[str, str]], file_reducer] 
