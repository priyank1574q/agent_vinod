WRITE_TODOS_DESCRIPTION = """Use this tool to create and manage a structured task list for your current work session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.
It also helps the user understand the progress of the task and overall progress of their requests.

## When to Use This Tool
Use this tool proactively in these scenarios:

1. Complex multi-step tasks - When a task requires 3 or more distinct steps or actions
2. Non-trivial and complex tasks - Tasks that require careful planning or multiple operations
3. User explicitly requests todo list - When the user directly asks you to use the todo list
4. User provides multiple tasks - When users provide a list of things to be done (numbered or comma-separated)
5. After receiving new instructions - Immediately capture user requirements as todos
6. When you start working on a task - Mark it as in_progress BEFORE beginning work. Ideally you should only have one todo as in_progress at a time
7. After completing a task - Mark it as completed and add any new follow-up tasks discovered during implementation

## When NOT to Use This Tool

Skip using this tool when:
1. There is only a single, straightforward task
2. The task is trivial and tracking it provides no organizational benefit
3. The task can be completed in less than 3 trivial steps
4. The task is purely conversational or informational

NOTE that you should not use this tool if there is only one trivial task to do. In this case you are better off just doing the task directly.

## Examples of When to Use the Todo List

# Add this new example block inside the WRITE_TODOS_DESCRIPTION string

<example>
User: I need a plot showing sales by category from the file 'data.csv'.
Assistant: I can generate that plot for you. First, I will create a to-do list to track the steps for this analysis.
*Creates todo list with the following items:*
1. Register the data file 'data.csv'
2. Load the data into a pandas DataFrame
3. Group data by category and calculate total sales
4. Create a bar plot of the results
5. Save the final plot to a file
*Begins working on the first task*

<reasoning>
The assistant used the todo list because:
1. Data analysis tasks involve multiple logical stages: loading, processing, visualizing, and saving.
2. Breaking the task down ensures each stage is handled correctly.
3. It provides the user with a clear plan of action before code is executed.
</reasoning>
</example>

<example>
User: I want to add a dark mode toggle to the application settings. Make sure you run the tests and build when you're done!
Assistant: I'll help add a dark mode toggle to your application settings. Let me create a todo list to track this implementation.
*Creates todo list with the following items:*
1. Create dark mode toggle component in Settings page
2. Add dark mode state management (context/store)
3. Implement CSS-in-JS styles for dark theme
4. Update existing components to support theme switching
5. Run tests and build process, addressing any failures or errors that occur
*Begins working on the first task*

<reasoning>
The assistant used the todo list because:
1. Adding dark mode is a multi-step feature requiring UI, state management, and styling changes
2. The user explicitly requested tests and build be run afterward
3. The assistant inferred that tests and build need to pass by adding "Ensure tests and build succeed" as the final task
</reasoning>
</example>

<example>
User: Help me plan a comprehensive marketing campaign for our new product launch, including social media, email marketing, and press releases.
Assistant: I'll help you plan a comprehensive marketing campaign for your product launch. Let me create a todo list to organize all the components.
*Creates todo list with the following items:*
1. Define target audience and key messaging
2. Create social media content calendar and posting schedule
3. Design email marketing sequence and automation flows
4. Draft press release and identify media contacts
5. Set up tracking and analytics for campaign performance
6. Create visual assets and brand materials
7. Coordinate launch timeline and deliverables
*Begins working on the first task*

<reasoning>
The assistant used the todo list because:
1. Marketing campaign planning involves multiple distinct channels and activities
2. Each component requires careful coordination and planning
3. The systematic approach ensures all aspects of the launch are covered
4. Progress tracking helps maintain timeline and deliverables
</reasoning>
</example>

<example>
User: Help me rename the function getCwd to getCurrentWorkingDirectory across my project
Assistant: Let me first search through your codebase to find all occurrences of 'getCwd'.
*Uses search tools to locate all instances of getCwd in the codebase*
Assistant: I've found 15 instances of 'getCwd' across 8 different files. Let me create a todo list to track these changes.
*Creates todo list with specific items for each file that needs updating*

<reasoning>
The assistant used the todo list because:
1. First, the assistant searched to understand the scope of the task
2. Upon finding multiple occurrences across different files, it determined this was a complex task with multiple steps
3. The todo list helps ensure every instance is tracked and updated systematically
4. This approach prevents missing any occurrences and maintains consistency
</reasoning>
</example>

<example>
User: I need help organizing my home office: decluttering the desk, setting up a filing system, organizing digital files, and creating a daily workflow.
Assistant: I'll help you organize your home office systematically. Let me create a todo list to track each area of organization.
*Creates todo list with items like: 1) Sort and declutter desk items, 2) Set up physical filing system for documents, 3) Organize digital files and folders, 4) Create daily workflow and productivity systems, 5) Establish maintenance routines*
Let's start with decluttering your desk space to create a clean foundation for the other organizational systems.

<reasoning>
The assistant used the todo list because:
1. The user provided multiple distinct organizational tasks
2. Each area requires different approaches and careful planning
3. Home organization benefits from systematic, step-by-step completion
4. Progress tracking ensures all areas are addressed thoroughly
</reasoning>
</example>

## Examples of When NOT to Use the Todo List

<example>
User: How do I print 'Hello World' in Python?
Assistant: In Python, you can print "Hello World" with this simple code:

python
print("Hello World")

This will output the text "Hello World" to the console when executed.</assistant>

<reasoning>
The assistant did not use the todo list because this is a single, trivial task that can be completed in one step. There's no need to track multiple tasks or steps for such a straightforward request.
</reasoning>
</example>

<example>
User: What's the best way to water houseplants?
Assistant: The best way to water houseplants depends on the specific plant type, but here are some general guidelines:

- Check soil moisture by inserting your finger about 1-2 inches into the soil
- Water thoroughly when the top inch feels dry, allowing water to drain from the bottom
- Use room temperature water and water in the morning when possible
- Avoid overwatering, which is more harmful than underwatering for most plants

Different plants have different needs, so it's important to research your specific varieties for optimal care.

<reasoning>
The assistant did not use the todo list because this is an informational request with no actual tasks to complete. The user is simply asking for advice and explanation, not for the assistant to perform multiple steps or activities.
</reasoning>
</example>

<example>
User: Can you add a comment to the calculateTotal function to explain what it does?
Assistant: Sure, let me add a comment to the calculateTotal function to explain what it does.
* Uses the Edit tool to add a comment to the calculateTotal function *

<reasoning>
The assistant did not use the todo list because this is a single, straightforward task confined to one location. Adding a comment doesn't require tracking multiple steps or systematic organization.
</reasoning>
</example>

<example>
User: What time is it in Tokyo right now?
Assistant: I'll check the current time in Tokyo for you.

*Searches for current time in Tokyo*

The current time in Tokyo, Japan is [current time]. Tokyo is in the Japan Standard Time (JST) zone, which is UTC+9.

<reasoning>
The assistant did not use the todo list because this is a single information lookup with immediate results. There are no multiple steps to track or organize, making the todo list unnecessary for this straightforward request.
</reasoning>
</example>

## Task States and Management

1. **Task States**: Use these states to track progress:
   - pending: Task not yet started
   - in_progress: Currently working on (limit to ONE task at a time)
   - completed: Task finished successfully

2. **Task Management**:
   - Update task status in real-time as you work
   - Mark tasks complete IMMEDIATELY after finishing (don't batch completions)
   - Only have ONE task in_progress at any time
   - Complete current tasks before starting new ones
   - Remove tasks that are no longer relevant from the list entirely

3. **Task Completion Requirements**:
   - ONLY mark a task as completed when you have FULLY accomplished it
   - If you encounter errors, blockers, or cannot finish, keep the task as in_progress
   - When blocked, create a new task describing what needs to be resolved
   - Never mark a task as completed if:
     - There are unresolved issues or errors
     - Work is partial or incomplete
     - You encountered blockers that prevent completion
     - You couldn't find necessary resources or dependencies
     - Quality standards haven't been met

4. **Task Breakdown**:
   - Create specific, actionable items
   - Break complex tasks into smaller, manageable steps
   - Use clear, descriptive task names

When in doubt, use this tool. Being proactive with task management demonstrates attentiveness and ensures you complete all requirements successfully."""

TASK_DESCRIPTION_PREFIX = """Launch a new agent to handle complex, multi-step tasks autonomously. 

Available agent types and the tools they have access to:
- general-purpose: General-purpose agent for researching complex questions, searching for files and content, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you. (Tools: *)
{other_agents}
"""

TASK_DESCRIPTION_SUFFIX = """When using the Task tool, you must specify a subagent_type parameter to select which agent type to use.

When to use the Agent tool:
- When you are instructed to execute custom slash commands. Use the Agent tool with the slash command invocation as the entire prompt. The slash command can take arguments. For example: Task(description="Check the file", prompt="/check-file path/to/file.py")

When NOT to use the Agent tool:
- If you want to read a specific file path, use the Read or Glob tool instead of the Agent tool, to find the match more quickly
- If you are searching for a specific term or definition within a known location, use the Glob tool instead, to find the match more quickly
- If you are searching for content within a specific file or set of 2-3 files, use the Read tool instead of the Agent tool, to find the match more quickly
- Other tasks that are not related to the agent descriptions above


Usage notes:
1. Launch multiple agents concurrently whenever possible, to maximize performance; to do that, use a single message with multiple tool uses
2. When the agent is done, it will return a single message back to you. The result returned by the agent is not visible to the user. To show the user the result, you should send a text message back to the user with a concise summary of the result.
3. Each agent invocation is stateless. You will not be able to send additional messages to the agent, nor will the agent be able to communicate with you outside of its final report. Therefore, your prompt should contain a highly detailed task description for the agent to perform autonomously and you should specify exactly what information the agent should return back to you in its final and only message to you.
4. The agent's outputs should generally be trusted
5. Clearly tell the agent whether you expect it to create content, perform analysis, or just do research (search, file reads, web fetches, etc.), since it is not aware of the user's intent
6. If the agent description mentions that it should be used proactively, then you should try your best to use it without the user having to ask for it first. Use your judgement.

Example usage:

<example_agent_descriptions>
"content-reviewer": use this agent after you are done creating significant content or documents
"greeting-responder": use this agent when to respond to user greetings with a friendly joke
"research-analyst": use this agent to conduct thorough research on complex topics
</example_agent_description>

<example>
user: "Please write a function that checks if a number is prime"
assistant: Sure let me write a function that checks if a number is prime
assistant: First let me use the Write tool to write a function that checks if a number is prime
assistant: I'm going to use the Write tool to write the following code:
<code>
function isPrime(n) {
  if (n <= 1) return false
  for (let i = 2; i * i <= n; i++) {
    if (n % i === 0) return false
  }
  return true
}
</code>
<commentary>
Since significant content was created and the task was completed, now use the content-reviewer agent to review the work
</commentary>
assistant: Now let me use the content-reviewer agent to review the code
assistant: Uses the Task tool to launch with the content-reviewer agent 
</example>

<example>
user: "Can you help me research the environmental impact of different renewable energy sources and create a comprehensive report?"
<commentary>
This is a complex research task that would benefit from using the research-analyst agent to conduct thorough analysis
</commentary>
assistant: I'll help you research the environmental impact of renewable energy sources. Let me use the research-analyst agent to conduct comprehensive research on this topic.
assistant: Uses the Task tool to launch with the research-analyst agent, providing detailed instructions about what research to conduct and what format the report should take
</example>

<example>
user: "Hello"
<commentary>
Since the user is greeting, use the greeting-responder agent to respond with a friendly joke
</commentary>
assistant: "I'm going to use the Task tool to launch with the greeting-responder agent"
</example>"""
# EDIT_DESCRIPTION = """Performs exact string replacements in files. 

# Usage:
# - You must use your `Read` tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file. 
# - When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: spaces + line number + tab. Everything after that tab is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
# - ALWAYS prefer editing existing files. NEVER write new files unless explicitly required.
# - Only use emojis if the user explicitly requests it. Avoid adding emojis to files unless asked.
# - The edit will FAIL if `old_string` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use `replace_all` to change every instance of `old_string`. 
# - Use `replace_all` for replacing and renaming strings across the file. This parameter is useful if you want to rename a variable for instance."""

EDIT_DESCRIPTION = """Performs precise edits on a file using different modes.
This tool automatically creates a one-time backup before any modification, which can be restored using the `undo_edit` tool.

MODES:
1. `replace`:
   - Replaces the first occurrence of `old_string` with `new_string`.
   - Required args: `file_path`, `mode='replace'`, `old_string`, `new_string`.

2. `regex_replace`:
   - Replaces all occurrences matching a regex pattern.
   - Required args: `file_path`, `mode='regex_replace'`, `old_string` (as the regex pattern), `new_string`.

3. `insert`:
   - Inserts `new_string` into the file on a new line.
   - Use EITHER `insert_line` (line number) OR `insert_after` (text from the line above) to specify location.
   - Required args: `file_path`, `mode='insert'`, `new_string`, and (`insert_line` or `insert_after`).
"""


TOOL_DESCRIPTION = """Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:
- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to 2000 lines starting from the beginning of the file
- You can optionally specify a line offset and limit (especially handy for long files), but it's recommended to read the whole file by not providing these parameters
- Any lines longer than 2000 characters will be truncated
- Results are returned using cat -n format, with line numbers starting at 1
- You have the capability to call multiple tools in a single response. It is always better to speculatively read multiple files as a batch that are potentially useful. 
- If you read a file that exists but has empty contents you will receive a system reminder warning in place of file contents."""

READ_TOOL_DESCRIPTION = """
Reads files from the local filesystem using various modes. This tool can operate on multiple files at once using glob patterns.

Usage:
- Provide a list of paths or glob patterns (e.g., ["src/main.py"], ["data/*.csv"]).
- Choose a 'mode' to specify the action to perform.

MODES:
1.  `find` (Default if no mode is provided):
    - Lists all files matching the given paths/patterns.
    - Example: `read_file(paths=["src/**/*"], mode="find")` to list all files in the src directory.

2.  `view`:
    - Reads and displays the content of the specified files.
    - Use `start_line` and `limit` to read parts of large files.
    - Example: `read_file(paths=["my_file.txt"], mode="view", start_line=100, limit=50)`

3.  `search`:
    - Searches for a specific `search_pattern` within the specified files.
    - Returns the lines that contain the pattern.
    - This mode REQUIRES the `search_pattern` argument.
    - Example: `read_file(paths=["*.py"], mode="search", search_pattern="def process_data")`

4.  `stats`:
    - Provides statistics for each file (e.g., line count, size in bytes).
    - Example: `read_file(paths=["data/large_dataset.csv"], mode="stats")`

You have the capability to call multiple tools in a single response. It is always better to speculatively read multiple files as a batch that are potentially useful.
"""

THINK_DESCRIPTION="""
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


PYTHON_REPL_DESCRIPTION = """Executes Python code in a stateful, interactive REPL (Read-Eval-Print Loop) session.

## Key Feature: Stateful Execution
Variables, functions, and dataframes defined in one call to this tool **will persist** to subsequent calls within the same session. This makes it ideal for iterative exploration.

## When to Use This Tool
- For **interactive exploration**: When you need to inspect intermediate data or variables step-by-step.
- For **debugging**: To test small snippets of code and diagnose issues without running a full script.
- For **quick experiments**: When you want to try a transformation or function call and immediately see the result.

## CRITICAL USAGE CONSTRAINT
This tool is **ONLY** for exploration and debugging. It **MUST NOT** be used to produce the final deliverables of a task (like saving plots or data files).

After using the REPL to figure out your approach, you **MUST** consolidate all the working steps into a **single, monolithic script** and execute it using the `execute_code` tool to produce the final output.

## Parameters
- `code` (str): The Python code to execute.
- `reset_state` (bool, optional): If `True`, it will clear the REPL's memory and start a fresh session. Use this when you want to start over.
"""

# Add this to your prompts.py file

GET_DATA_DICTIONARY_DESCRIPTION = """
Analyzes the project's datasets to provide a detailed data dictionary. Can return the full
dictionary for all tables, the schema for a single table, or the definition for a single column.
It efficiently caches the full dictionary after the first run to avoid repeated file reads.

Use this tool as one of the first steps to understand the data's structure, available columns,
data types, and relationships between tables. This is crucial for planning your analysis.
Currently data dictionary is for data (order_data,cart_adds,clicks,impression,catalog)

Examples:
- To get the full dictionary for all tables: `get_data_dictionary()`
- To get the schema for only the 'order_data' table: `get_data_dictionary(table_name='order_data')`
- To get the definition of the 'revenue' column in 'order_data': `get_data_dictionary(table_name='order_data', column_name='revenue')`
"""
