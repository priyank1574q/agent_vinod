from fastapi import FastAPI
from pydantic import BaseModel

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional, Literal, Union
from typing_extensions import Annotated
from typing_extensions import TypedDict, NotRequired
from datetime import datetime, timedelta
import traceback
import difflib
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')



from deepagents.graph import create_deep_agent
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from typing import Annotated
from langgraph.prebuilt import InjectedState

from deepagents.sub_agent import _create_task_tool, SubAgent
from deepagents.model import get_default_model
# ,get_gemini
from deepagents.tools import write_todos, write_file, read_file, ls, edit_file,think,execute_code,register_file,python_repl,read_image,undo_edit,get_data_dictionary
from deepagents.state import DeepAgentState
from typing import Sequence, Union, Callable, Any, TypeVar, Type, Optional
from langchain_core.tools import BaseTool
from langchain_core.language_models import LanguageModelLike

from langgraph.prebuilt import create_react_agent

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import datetime
import re
import time




import json
import traceback
import sys
from io import StringIO, BytesIO
import base64
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from typing import Annotated
from langgraph.prebuilt import InjectedState
from deepagents.state import DeepAgentState
import io
from contextlib import redirect_stdout
# Import existing deepagents tools
from langgraph.checkpoint.memory import InMemorySaver
import uuid

from deepagents.graph import create_deep_agent
# Assuming your create_deep_agent is in the `deepagents` directory.
# You will need to adjust the import based on your project structure.


app = FastAPI()

extra_tools=[think,execute_code,register_file,python_repl,read_image,undo_edit]
checkpointer = InMemorySaver()

base_path="/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/outputs"

prompt_file_path = os.path.join("/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/deepagents/coding_prompt", "coding_prompt_v4.md")

with open(prompt_file_path, 'r') as f:
    prompt_template = f.read()

# 2. Inject the base_path variable using .format()
coding_instructions = prompt_template.format(base_path=base_path)

creds_dir = "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/deepagents/creds"

with open(creds_path_local, "r") as f:
    loaded_creds_from_file = json.load(f)


# This should be adapted to your specific tools and instructions
agent = create_deep_agent(
    loaded_creds=loaded_creds,
    # model=llm_gem_flash,
    tools=extra_tools,
    instructions=coding_instructions,
    checkpointer=checkpointer,
    max_tokens=512

).with_config({"recursion_limit": 50})


class Request(BaseModel):
    messages: list


@app.post("/invoke")
async def invoke(request: Request):
    """
    This endpoint will be called by the UI to interact with the agent.
    """
    # This is a simplified example. You'll need to adapt this to handle
    # the state and streaming correctly, as expected by the UI.
    # The UI uses the @langchain/langgraph-sdk, which expects a streaming endpoint.
    # You might need to implement Server-Sent Events (SSE) for a fully compatible streaming response.
    last_message = ""
    async for s in agent.astream(request.dict()):
        last_message = s

    return last_message