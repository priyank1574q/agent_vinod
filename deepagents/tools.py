from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from typing import Annotated, Dict, Any,List,Literal,Optional
from langgraph.prebuilt import InjectedState
import io
from contextlib import redirect_stdout
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import re
import os
import random
import json
import time
import glob
from langchain_core.pydantic_v1 import BaseModel, Field

from deepagents.prompts import (
    WRITE_TODOS_DESCRIPTION,
    EDIT_DESCRIPTION,
    TOOL_DESCRIPTION,
    THINK_DESCRIPTION,
    READ_TOOL_DESCRIPTION,
    PYTHON_REPL_DESCRIPTION,
    GET_DATA_DICTIONARY_DESCRIPTION
)
from deepagents.state import Todo, DeepAgentState

@tool
def register_file(
    file_path: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    Verifies that a file exists at the given path and adds it to the agent's
    internal file memory. This MUST be the first step before reading or analyzing
    any file provided by the user.
    """
    if not os.path.exists(file_path):
        return Command(
            update={
                "messages": [
                    ToolMessage(f"Error: File not found at '{file_path}'. Please verify the path.", tool_call_id=tool_call_id)
                ]
            }
        )

    # For simplicity, we add a placeholder content. The actual reading will be done by pandas.
    files = state.get("files", {})
    files[file_path] = f"User-provided file, verified to exist at {datetime.now().isoformat()}."
    
    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(f"Successfully registered file: {file_path}", tool_call_id=tool_call_id)
            ]
        }
    )

# # The Pydantic schema for write_todos
# class TodoModel(BaseModel):
#     content: str = Field(description="The description of the task.")
#     status: Literal["pending", "in_progress", "completed"] = Field(description="The current status of the task.")

# class WriteTodosSchema(BaseModel):
#     todos: List[TodoModel] = Field(description="A complete list of to-do items to set as the new task list.")


@tool(description=WRITE_TODOS_DESCRIPTION)
def write_todos(
    todos: list[Todo], tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(f"Updated todo list to {todos}", tool_call_id=tool_call_id)
            ],
        }
    )



# @tool(description=WRITE_TODOS_DESCRIPTION)
# def write_todos(
#     state: Annotated[DeepAgentState, InjectedState],
#     tool_call_id: Annotated[str, InjectedToolCallId],
#     todos: list[dict]
#     # The 'todos' argument comes from the schema
# ) -> Command:
#     return Command(
#         update={
#             "todos": todos,
#             "messages": [
#                 ToolMessage(f"Updated todo list to {todos}", tool_call_id=tool_call_id)
#             ],
#         }
#     )


def ls(state: Annotated[DeepAgentState, InjectedState]) -> list[str]:
    """List all files"""
    return list(state.get("files", {}).keys())



# Define an arguments schema for the tool
# class ReadFileSchema(BaseModel):
#     paths: List[str] = Field(description="A list of file paths or glob patterns to target.")
#     mode: Literal['view', 'find', 'search', 'stats'] = Field(
#         default='view',
#         description="The mode of operation."
#     )
#     search_pattern: str | None = Field(
#         default=None,
#         description="The string pattern to search for in 'search' mode."
#     )
#     start_line: int = Field(
#         default=0,
#         description="The starting line number for 'view' mode."
#     )
#     limit: int = Field(
#         default=2000,
#         description="The maximum number of lines or results to return."
#     )

# Pass the schema to the @tool decorator


@tool(description=READ_TOOL_DESCRIPTION,) 
def read_file(
    # Arguments from the schema
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    paths: list[str],
    mode: str = "view",
    search_pattern: str = None,
    start_line: int = 0,
    limit: int = 4000
) -> Command:
    """
    Advanced file reading tool with multiple modes.

    Args:
        paths (list[str]): A list of file paths or glob patterns.
        mode (str): The mode of operation. One of ['view', 'find', 'search', 'stats'].
        search_pattern (str): The string pattern to search for in 'search' mode.
        recursive (bool): Whether to search directories recursively in 'find' mode.
        start_line (int): The starting line number for 'view' mode.
        limit (int): The maximum number of lines to read in 'view' mode.
    """
    mock_filesystem = state.get("files", {})
    all_found_files = set()

    # 1. Expand all paths and glob patterns to get a list of files
    for path_pattern in paths:
        if "*" in path_pattern or "?" in path_pattern:
            # Use glob for wildcard patterns on the mock filesystem keys
            matched_files = [
                f for f in mock_filesystem.keys() if glob.fnmatch.fnmatch(f, path_pattern)
            ]
            all_found_files.update(matched_files)
        elif os.path.isdir(path_pattern):
             # For directories, find all files within them if recursive is True
             if recursive:
                 for f_path in mock_filesystem.keys():
                     if f_path.startswith(path_pattern):
                         all_found_files.add(f_path)
        elif path_pattern in mock_filesystem:
            all_found_files.add(path_pattern)

    final_files = sorted(list(all_found_files))

    if not final_files and mode != 'find':
        return Command(update={"messages": [ToolMessage(f"Error: No files found matching patterns: {paths}", tool_call_id=tool_call_id)]})

    output_lines = []

    # 2. Execute logic based on the selected mode
    if mode == "find":
        if not final_files:
             output_lines.append(f"No files found matching: {', '.join(paths)}")
        else:
            output_lines.append(f"Found {len(final_files)} files:")
            output_lines.extend(final_files)

    elif mode == "view":
        for file_path in final_files:
            content = mock_filesystem.get(file_path, f"Error: File '{file_path}' not found in state.")
            if content.startswith("Error:"):
                output_lines.append(content)
                continue
            
            lines = content.splitlines()
            end_line = min(start_line + limit, len(lines))
            output_lines.append(f"--- Content of {file_path} (lines {start_line+1}-{end_line}) ---")
            
            for i in range(start_line, end_line):
                line_content = lines[i]
                if len(line_content) > 2000:
                    line_content = line_content[:2000] + " [TRUNCATED]"
                output_lines.append(f"{i+1:6d}\t{line_content}")

    elif mode == "search":
        if not search_pattern:
            return Command(update={"messages": [ToolMessage("Error: 'search_pattern' is required for search mode.", tool_call_id=tool_call_id)]})
        
        output_lines.append(f"Searching for '{search_pattern}' in {len(final_files)} file(s)...")
        total_matches = 0
        for file_path in final_files:
            matches_in_file = []
            content = mock_filesystem.get(file_path)
            if not content: continue

            for i, line in enumerate(content.splitlines()):
                if search_pattern in line:
                    matches_in_file.append(f"  {i+1:6d}: {line.strip()}")
            
            if matches_in_file:
                total_matches += len(matches_in_file)
                output_lines.append(f"\nMatches in {file_path}:")
                output_lines.extend(matches_in_file)
        
        output_lines.append(f"\n--- Search complete. Found {total_matches} total matches. ---")

    elif mode == "stats":
        output_lines.append("--- File Statistics ---")
        for file_path in final_files:
            content = mock_filesystem.get(file_path)
            if not content:
                output_lines.append(f"\n{file_path}:\n  Error: Could not read file.")
                continue
            
            line_count = len(content.splitlines())
            size_bytes = len(content.encode('utf-8'))
            output_lines.append(f"\n{file_path}:")
            output_lines.append(f"  - Line Count: {line_count}")
            output_lines.append(f"  - Size: {size_bytes} bytes (~{size_bytes/1024:.2f} KB)")

    else:
        return Command(update={"messages": [ToolMessage(f"Error: Invalid mode '{mode}'. Available modes: find, view, search, stats.", tool_call_id=tool_call_id)]})

    final_output = "\n".join(output_lines)
    return Command(update={"messages": [ToolMessage(f"File operation result:\n```\n{final_output}\n```", tool_call_id=tool_call_id)]})

# Important: Remove the old `read_file` function if you haven't already.


# @tool(description=TOOL_DESCRIPTION)
# def read_file(
#     file_path: str,
#     state: Annotated[DeepAgentState, InjectedState],
#     offset: int = 0,
#     limit: int = 2000,
# ) -> str:
#     """Read file."""
#     mock_filesystem = state.get("files", {})
#     if file_path not in mock_filesystem:
#         return f"Error: File '{file_path}' not found"
#     content = mock_filesystem[file_path]
#     if not content or content.strip() == "":
#         return "System reminder: File exists but has empty contents"
#     lines = content.splitlines()
#     start_idx = offset
#     end_idx = min(start_idx + limit, len(lines))
#     if start_idx >= len(lines):
#         return f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"
#     result_lines = []
#     for i in range(start_idx, end_idx):
#         line_content = lines[i]
#         if len(line_content) > 2000:
#             line_content = line_content[:2000]
#         line_number = i + 1
#         result_lines.append(f"{line_number:6d}\t{line_content}")
#     return "\n".join(result_lines)


def write_file(
    file_path: str,
    content: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Write to a file."""
    files = state.get("files", {})
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update the files dictionary
        files[file_path] = content
        
        print(f"Successfully saved content to {file_path}")
    
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")

    

    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(f"Updated file {file_path}", tool_call_id=tool_call_id)
            ],
        }
    )




# @tool(description=EDIT_DESCRIPTION)
# def edit_file(
#     file_path: str,
#     old_string: str,
#     new_string: str,
#     state: Annotated[DeepAgentState, InjectedState],
#     tool_call_id: Annotated[str, InjectedToolCallId],
#     replace_all: bool = False,
# ) -> str:
#     """Write to a file."""
#     mock_filesystem = state.get("files", {})
#     if file_path not in mock_filesystem:
#         return f"Error: File '{file_path}' not found"
#     content = mock_filesystem[file_path]
#     if old_string not in content:
#         return f"Error: String not found in file: '{old_string}'"
#     if not replace_all:
#         occurrences = content.count(old_string)
#         if occurrences > 1:
#             return f"Error: String '{old_string}' appears {occurrences} times in file. Use replace_all=True to replace all instances, or provide a more specific string with surrounding context."
#         elif occurrences == 0:
#             return f"Error: String not found in file: '{old_string}'"
#     if replace_all:
#         new_content = content.replace(old_string, new_string)
#     else:
#         new_content = content.replace(old_string, new_string, 1)
#     mock_filesystem[file_path] = new_content
#     return Command(
#         update={
#             "files": mock_filesystem,
#             "messages": [
#                 ToolMessage(f"Updated file {file_path}", tool_call_id=tool_call_id)
#             ],
#         }
#     )

# 1. Define the arguments schema for edit_file
class EditFileSchema(BaseModel):
    file_path: str = Field(description="The path to the file to be edited.")
    mode: str = Field(description="The edit mode. Must be one of 'replace', 'insert', or 'regex_replace'.")
    old_string: str | None = Field(default=None, description="The string to be replaced or the regex pattern. Required for 'replace' and 'regex_replace' modes.")
    new_string: str | None = Field(default=None, description="The new string to insert or replace with.")
    insert_line: int | None = Field(default=None, description="The line number at which to insert the new_string. Used in 'insert' mode.")
    insert_after: str | None = Field(default=None, description="A substring in the file. The new_string will be inserted on the line immediately after the first occurrence of this substring. Used in 'insert' mode.")



@tool(description=EDIT_DESCRIPTION, args_schema=EditFileSchema)
def edit_file(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    file_path: str,
    mode: str, # 'replace', 'insert', or 'regex_replace'
    old_string: str = None,
    new_string: str = None,
    insert_line: int = None,
    insert_after: str = None,
) -> Command:
    """
    Edits a file with various modes: replace, insert, or regex_replace.
    This tool automatically creates a backup before modification, which can be
    restored with the 'undo_edit' tool.
    """
    mock_filesystem = state.get("files", {})
    if file_path not in mock_filesystem:
        return Command(update={"messages": [ToolMessage(f"Error: File '{file_path}' not found", tool_call_id=tool_call_id)]})

    # --- Backup Mechanism ---
    # Before any changes, save the current content to the backup state
    current_content = mock_filesystem[file_path]
    backups = state.get("files_backup", {})
    backups[file_path] = current_content
    # ---

    new_content = ""
    if mode == "replace":
        if not all([old_string, new_string is not None]):
            return Command(update={"messages": [ToolMessage("Error: 'old_string' and 'new_string' are required for replace mode.", tool_call_id=tool_call_id)]})
        if old_string not in current_content:
            return Command(update={"messages": [ToolMessage(f"Error: String not found in file: '{old_string}'", tool_call_id=tool_call_id)]})
        new_content = current_content.replace(old_string, new_string)

    elif mode == "regex_replace":
        if not all([old_string, new_string is not None]):
            return Command(update={"messages": [ToolMessage("Error: 'old_string' (as pattern) and 'new_string' are required for regex_replace mode.", tool_call_id=tool_call_id)]})
        try:
            new_content, count = re.subn(old_string, new_string, current_content)
            if count == 0:
                return Command(update={"messages": [ToolMessage(f"Error: Regex pattern '{old_string}' found 0 matches.", tool_call_id=tool_call_id)]})
        except re.error as e:
            return Command(update={"messages": [ToolMessage(f"Error: Invalid Regex pattern: {e}", tool_call_id=tool_call_id)]})

    elif mode == "insert":
        if new_string is None or (insert_line is None and insert_after is None):
            return Command(update={"messages": [ToolMessage("Error: 'new_string' and either 'insert_line' or 'insert_after' are required for insert mode.", tool_call_id=tool_call_id)]})
        
        lines = current_content.splitlines()
        insertion_point = -1

        if insert_line is not None:
            if 0 <= insert_line <= len(lines):
                insertion_point = insert_line
            else:
                 return Command(update={"messages": [ToolMessage(f"Error: Line number {insert_line} is out of range.", tool_call_id=tool_call_id)]})
        elif insert_after:
            for i, line in enumerate(lines):
                if insert_after in line:
                    insertion_point = i + 1
                    break
            if insertion_point == -1:
                return Command(update={"messages": [ToolMessage(f"Error: Text '{insert_after}' to insert after was not found.", tool_call_id=tool_call_id)]})
        
        lines.insert(insertion_point, new_string)
        new_content = "\n".join(lines)

    else:
        return Command(update={"messages": [ToolMessage(f"Error: Invalid mode '{mode}'. Use 'replace', 'insert', or 'regex_replace'.", tool_call_id=tool_call_id)]})
    
    mock_filesystem[file_path] = new_content
    return Command(
        update={
            "files": mock_filesystem,
            "files_backup": backups, # Persist the backup
            "messages": [
                ToolMessage(f"Successfully edited file: {file_path}", tool_call_id=tool_call_id)
            ],
        }
    )

@tool
def undo_edit(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    file_path: str,
) -> Command:
    """
    Undoes the most recent change to a file by restoring it from the backup.
    """
    backups = state.get("files_backup", {})
    if file_path not in backups:
        return Command(update={"messages": [ToolMessage(f"Error: No backup found for file '{file_path}'.", tool_call_id=tool_call_id)]})

    mock_filesystem = state.get("files", {})
    
    # Restore the content from backup
    restored_content = backups[file_path]
    mock_filesystem[file_path] = restored_content

    # Optionally, clear the backup for this file after restoring
    del backups[file_path]

    return Command(
        update={
            "files": mock_filesystem,
            "files_backup": backups,
            "messages": [
                ToolMessage(f"Successfully reverted changes to file: {file_path}", tool_call_id=tool_call_id)
            ]
        }
    )


# In tools.py
@tool
def execute_code(
    code: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    Execute Python code and return the output. This tool automatically detects
    file creations and updates the internal file state.
    Execute Python code and return the output. This tool automatically detects
    file creations (e.g., using df.to_csv, plt.savefig) in specified output
    directories and updates the internal file state. Core libraries like
    pandas (as pd) and numpy (as np) are pre-imported.
    """
    # Regex to find directories mentioned in the code, which we'll monitor for new files.
    # This looks for string literals like '/path/to/something/'
    potential_dirs = set(re.findall(r"['\"](/[^'\"]+/)['\"]", code))

    # Also consider the current working directory if no specific dirs are found.
    # In many environments, this is a default output location.
    # For this example, let's add the base path from your prompt as a default.
    base_output_dir = "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/outputs"
    potential_dirs.add(base_output_dir)

    # --- New Logic: Monitor directories for changes ---
    files_before = {}
    for directory in potential_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            try:
                # Store the list of files that exist BEFORE the code runs
                files_before[directory] = set(os.listdir(directory))
            except OSError:
                pass

    local_vars = {}
    available_globals = {
        "pd": pd, "np": np, "plt": plt, "sns": sns,
        "datetime": datetime, "timedelta": timedelta, "re": re, "json": json,
        "os": os, "time": time
    }
    
    output_buffer = io.StringIO()
    execution_error = None

    try:
        with redirect_stdout(output_buffer):
            exec(code, available_globals, local_vars)
    # --- START: Upgraded Error Handling ---
    except NameError as e:
        execution_error = e
        # Provide a more instructive error message for NameErrors
        output_buffer.write(
            f"\n\nCRITICAL HINT: Execution failed because a variable was not defined ({e}). "
            "REMINDER: The code execution environment is stateless. You MUST define all variables, "
            "including loading data into dataframes (e.g., 'df = pd.read_csv(...)'), "
            "inside every single `execute_code` call."
        )
    # --- END: Upgraded Error Handling ---
    except Exception as e:
        execution_error = e

    # --- New Logic: Detect newly created files ---
    newly_created_files = {}
    for directory in potential_dirs:
        if os.path.exists(directory) and directory in files_before:
            try:
                files_after = set(os.listdir(directory))
                # The difference between the two sets is our new files
                new_filenames = files_after - files_before.get(directory, set())
                for filename in new_filenames:
                    full_path = os.path.join(directory, filename)
                    try:
                        # Read the content of each new file to update the state
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        newly_created_files[full_path] = content
                    except (UnicodeDecodeError, IsADirectoryError):
                        # For binary files (like images) or subdirectories, just note their existence.
                        newly_created_files[full_path] = f"Binary content or directory at {full_path}"
                    except Exception as e:
                        newly_created_files[full_path] = f"Error reading file: {e}"
            except Exception as e:
                print(f"Warning: Could not scan directory {directory} for changes: {e}")
    
    output = output_buffer.getvalue()
    if execution_error:
        output = f"Error executing code: {execution_error}\n{output}"
    elif not output.strip():
        # If there's no printed output, provide a success message
        if newly_created_files:
            output = f"Code executed successfully. Detected {len(newly_created_files)} new file(s)."
        else:
            output = "Code executed successfully with no new files detected."

    # Merge the newly created files with the existing files in the state
    updated_files = {**state.get("files", {}), **newly_created_files}
    print("newly_created_files:",newly_created_files)

    return Command(
        update={
            "files": updated_files,
            "messages": [
                ToolMessage(f"Code execution output:\n```\n{output}\n```", tool_call_id=tool_call_id)
            ]
        }
    )

@tool(description=PYTHON_REPL_DESCRIPTION)
def python_repl(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    code: str,
    reset_state: bool = False,
) -> Command:
    """
    Executes Python code in a persistent REPL session. Variables, functions,
    and imports are remembered across calls.
    Args:
        code (str): The Python code to execute.
        reset_state (bool): If True, clears the session's memory before executing.
    """
    namespace = state.get("python_namespace", {})

    if reset_state:
        namespace = {}

    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(code, namespace)
    except Exception as e:
        output_buffer.write(f"\nError executing code: {e}")

    output = output_buffer.getvalue()
    if not output.strip():
        output = "Code executed successfully with no output."

    return Command(
        update={
            "python_namespace": namespace, # Persist the updated namespace
            "messages": [
                ToolMessage(f"REPL output:\n```\n{output}\n```", tool_call_id=tool_call_id)
            ]
        }
    )

# Make sure to import these at the top of tools.py
import base64
import os
from PIL import Image

@tool
def read_image(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    file_path: str,
) -> Command:
    """
    Reads an image file, encodes it to a Base64 Data URI, and loads it into memory.
    This prepares the image to be sent to a vision model.
    """
    if not os.path.exists(file_path):
        return Command(update={"messages": [ToolMessage(f"Error: File not found at '{file_path}'.", tool_call_id=tool_call_id)]})

    try:
        # Determine the image format
        with Image.open(file_path) as img:
            format = img.format.lower()
            if format not in ['png', 'jpeg', 'gif', 'webp']:
                format = 'png' # Default to png if format is unknown or exotic
        
        # Read the raw bytes
        with open(file_path, "rb") as f:
            image_bytes = f.read()
        
        # Encode bytes to Base64
        encoded_string = base64.b64encode(image_bytes).decode('utf-8')

        # Create the full Data URI
        data_uri = f"data:image/{format};base64,{encoded_string}"

        images = state.get("images", {})
        images[file_path] = data_uri

        return Command(
            update={
                "images": images,
                "messages": [
                    ToolMessage(f"Successfully loaded image '{file_path}' into memory. It is now ready for analysis.", tool_call_id=tool_call_id)
                ]
            }
        )
    except Exception as e:
        return Command(update={"messages": [ToolMessage(f"Error reading image file: {e}", tool_call_id=tool_call_id)]})



# A simple `think` tool for planning
@tool(description=THINK_DESCRIPTION)
def think(
    thought: str,
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """
    Use this tool to think about complex reasoning or brainstorming during EDA analysis.
    
    Use it when you need to:
    - Analyze data understanding results and plan next steps
    - Process code execution outputs and plan fixes
    - Brainstorm different approaches to data analysis
    - Verify that your analysis plan addresses the user's requirements
    - Check if all required information has been collected
    - Reflect on analysis results before presenting to user
    - Plan which visualizations would be most valuable
    - Determine if analysis is complete or needs more work
    
    Examples for EDA:
    - After data understanding: "The dataset has 1000 rows and 15 columns with target variable 'price'. I should focus on correlation analysis and missing value patterns..."
    - After code execution: "The correlation heatmap shows strong relationships between income and spending. I should create scatter plots to visualize these relationships..."
    - Before final response: "I've completed basic EDA and correlation analysis. Let me verify I addressed the user's request for customer segmentation patterns..."
    """
    return Command(
        update={
            "messages": [
                ToolMessage(f"💭 Thinking: {thought}", tool_call_id=tool_call_id)
            ]
        }
    )




# --- NEW: Caching Logic ---
# This global variable will act as a simple in-memory cache.
_cached_data_dictionary = None

@tool(description=GET_DATA_DICTIONARY_DESCRIPTION)
def get_data_dictionary(
    table_name: Annotated[Optional[str], "The specific table to get the schema for."] = None,
    column_name: Annotated[Optional[str], "The specific column to get the definition for. Requires table_name."] = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None
) -> Command:
    """
    Analyzes datasets to provide a detailed data dictionary. Can return the full
    dictionary, the schema for a single table, or the definition for a single column.
    It efficiently caches the full dictionary after the first run to avoid repeated file reads.

    Examples:
    - To get the full dictionary: get_data_dictionary()
    - To get schema for 'orders' table: get_data_dictionary(table_name='order_data')
    - To get definition of 'revenue' column in 'orders': get_data_dictionary(table_name='order_data', column_name='revenue')
    """
    global _cached_data_dictionary

    # --- NEW: Caching Logic ---
    # If the dictionary is not cached, generate it.
    if _cached_data_dictionary is None:
        # This print statement is for demonstration to show when the expensive operation runs.
        print("--- Generating and caching data dictionary for the first time... ---")
        
        # IMPORTANT: Update these paths to point to your actual data files.
        file_paths = {
            "order_data": "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/benchmark/private/data/order_data.csv",
            "cart_adds": "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/benchmark/private/data/cart_adds.csv",
            "clicks": "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/benchmark/private/data/clicks.csv",
            "impression": "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/benchmark/private/data/impression1M_pdf.csv",
            "catalog": "/Workspace/Users/ayush.agarwal@nykaa.com/EDA_Agent/eda_agent_v2/deepagent_hackathon/benchmark/private/data/catalog.csv",
        }

        # (The rest of your data loading and schema generation logic remains the same here)
        # ...
        # --- Start of existing logic ---
        schema_config = {
            "order_data": {
                "order_purchased_date": {"desc": "The date when the order was placed by the customer."},
                "product_id": {"desc": "Identifier for the product in the order.", "joins": ["catalog.product_id", "cart_adds.product_id", "clicks.product_id", "impression.product_id"]},
                "customer_id": {"desc": "Identifier for the customer who placed the order.", "joins": ["cart_adds.customer_id", "clicks.customer_id", "impression.customer_id"]},
                "order_id": {"desc": "Unique identifier for the order transaction."},
                "revenue": {"desc": "Total revenue generated from the product in the order."},
                "qty": {"desc": "Quantity of the product ordered."},
                "order_timestamp": {"desc": "The exact timestamp when the order was placed."},
            },
            "cart_adds": {
                "product_id": {"desc": "Identifier for the product added to the cart.", "joins": ["catalog.product_id", "order_data.product_id","impression.product_id"]},
                "cust_hit_time_ist": {"desc": "Timestamp of the user action (add to cart) in IST."},
                "customer_id": {"desc": "Identifier for the customer.", "joins": ["order_data.customer_id","impression.customer_id"]},
                "session_id": {"desc": "Identifier for the user's session.", "joins": ["clicks.session_id", "impression.session_id"]},
                "product_brand": {"desc": "Brand name of the product."},
                "product_name": {"desc": "Name of the product."},
                "product_position": {"desc": "The numbered position of the product on the listing page where the event occurred."},
                "listing_position": {"desc": "The overall position in the product listing."},
                "nykaa_vertical": {"desc": "The business vertical on the Nykaa platform. (beauty is nykaa, fashion is nykaafashion)"},
                "nykaa_platform": {"desc": "The platform where the event occurred. (eg, ios or android)"},
                "event_name": {"desc": "The name of the tracking event (e.g., 'add_to_cart')."},
                "dn_tile_id": {"desc": "Internal tracking ID for the UI/widget tiles."},
                "dn_page_section": {"desc": "The section of the page(like UI/widget) where the event happened."},
                "date": {"desc": "The date of the event."},
                "_search_term": {"desc": "The search term used by the customer, if any."},
            },
            "clicks": {
                "product_id": {"desc": "Identifier for the clicked product.", "joins": ["catalog.product_id", "order_data.product_id","impression.product_id"]},
                "cust_hit_time_ist": {"desc": "Timestamp of the click event in IST."},
                "customer_id": {"desc": "Identifier for the customer.", "joins": ["order_data.customer_id","impression.customer_id","cart_adds.customer_id"]},
                "session_id": {"desc": "Identifier for the user's session.", "joins": ["cart_adds.session_id", "impression.session_id"]},
                "product_brand": {"desc": "Brand name of the product."},
                "product_name": {"desc": "Name of the product."},
                "product_position": {"desc": "The position of the product on the page when clicked."},
                "listing_position": {"desc": "The overall position in the product listing."},
                "nykaa_vertical": {"desc": "The business vertical on the Nykaa platform. (beauty is nykaa, fashion is nykaafashion)"},
                "nykaa_platform": {"desc": "The platform where the event occurred. (eg, ios or android)"},
                "event_name": {"desc": "The name of the tracking event (e.g., 'product_click')."},
                "dn_tile_id": {"desc": "Internal tracking ID for the UI/widget tiles."},
                "dn_page_section": {"desc": "The section of the page(like UI/widget) where the event happened."},
                "_search_term": {"desc": "The search term used by the customer, if any."},
            },
            "impression": {
                "product_id": {"desc": "Identifier for the product that was viewed.", "joins": ["catalog.product_id", "order_data.product_id","cart_adds.product_id","clicks.product_id"]},
                "date": {"desc": "Date of the impression."},
                "customer_id": {"desc": "Identifier for the customer who saw the impression.", "joins": [["order_data.customer_id","cart_adds.customer_id"]]},
                "product_position": {"desc": "The position of the product on the page."},
                "listing_position": {"desc": "The overall position in the product listing."},
                "_search_term": {"desc": "The search term that led to the impression."},
                "_category_id": {"desc": "Category ID associated with the search/listing."},
                "_brand_id": {"desc": "Brand ID associated with the search/listing.", "joins": ["catalog.brand_id"]},
                "_filters_str": {"desc": "Filters applied by the user as a string."},
                "_sort": {"desc": "The sorting option used."},
                "_search_redirection": {"desc": "Indicates if the search led to a redirection."},
                "nykaa_platform": {"desc": "The platform where the event occurred. (eg, ios or android)"},
                "session_id": {"desc": "Identifier for the user's session.", "joins": ["cart_adds.session_id", "clicks.session_id"]},
                "product_impressions": {"desc": "The event name for product impressions."},
                "tracking_metadata": {"desc": "Additional metadata for tracking."},
            },
            "catalog": {
                "product_id": {"desc": "Unique identifier for each product. Primary Key.", "joins": ["order_data.product_id", "cart_adds.product_id", "clicks.product_id", "impression.product_id"]},
                "parent_id": {"desc": "Identifier for the parent product if it's a variant."},
                "page_id": {"desc": "Internal page identifier."},
                "page_name": {"desc": "URL-friendly page name."},
                "popularity": {"desc": "A score indicating the product's popularity."},
                "in_stock": {"desc": "Flag indicating stock availability (1 for in stock, 0 for out of stock)."},
                "brand_id": {"desc": "Unique identifier for the brand."},
                "is_visible": {"desc": "Flag indicating if the product is visible on the site."},
                "first_image_url": {"desc": "URL of the primary product image."},
                "brand": {"desc": "Brand name."},
                "primary_l1": {"desc": "Level 1 category (e.g., 'Makeup')."},
                "primary_l2": {"desc": "Level 2 category (e.g., 'Face')."},
                "primary_l3": {"desc": "Level 3 category (e.g., 'Foundation')."},
                "season": {"desc": "Associated season (e.g., 'Summer')."},
                "gender": {"desc": "Target gender for the product."},
                "price_inr": {"desc": "Price of the product in Indian Rupees (INR)."},
                "title": {"desc": "The display title of the product."},
                "description": {"desc": "Detailed product description."},
                "size": {"desc": "Size of the product."},
            }
        }
        full_schema = {}
        dataframes = {}

        for name, path in file_paths.items():
            try:
                dataframes[name] = pd.read_csv(path, parse_dates=True, infer_datetime_format=True)
            except FileNotFoundError:
                return Command(update={"messages": [ToolMessage(f"Error: Data file not found at '{path}'. Cannot generate data dictionary.", tool_call_id=tool_call_id)]})
            except Exception as e:
                return Command(update={"messages": [ToolMessage(f"Error reading {path}: {e}", tool_call_id=tool_call_id)]})

        for name, df in dataframes.items():
            table_schema = {}
            total_rows = len(df)
            for col in df.columns:
                dtype = str(df[col].dtype)
                col_type = 'integer' if 'int' in dtype else 'float' if 'float' in dtype else 'datetime' if 'datetime' in dtype else 'string'
                examples = [str(val) for val in df[col].dropna().unique()[:3]]
                missing_pct = round((df[col].isnull().sum() / total_rows) * 100, 2) if total_rows > 0 else 0
                col_config = schema_config.get(name, {}).get(col, {})
                table_schema[col] = {
                    "type": col_type,
                    "description": col_config.get("desc", "No description available."),
                    "example_values": examples,
                    "unique_values": df[col].nunique(),
                    "missing_percentage": f"{missing_pct}%",
                    "joins_with": col_config.get("joins", [])
                }
            full_schema[name] = table_schema
        # --- End of existing logic ---

        _cached_data_dictionary = full_schema
    
    # --- NEW: Granularity Logic ---
    # Now, serve the request from the cached dictionary.
    if table_name and column_name:
        # User wants a single column's definition
        if table_name in _cached_data_dictionary and column_name in _cached_data_dictionary[table_name]:
            output = _cached_data_dictionary[table_name][column_name]
        else:
            output = {"error": f"Column '{column_name}' or table '{table_name}' not found."}
    elif table_name:
        # User wants a single table's schema
        if table_name in _cached_data_dictionary:
            output = _cached_data_dictionary[table_name]
        else:
            output = {"error": f"Table '{table_name}' not found."}
    else:
        # User wants the entire dictionary
        output = _cached_data_dictionary

    # Convert the selected output to a JSON string for the message
    output_json = json.dumps(output, indent=2)

    return Command(
        update={
            "messages": [
                ToolMessage(
                    f"Data dictionary information:\n\n```json\n{output_json}\n```",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    )