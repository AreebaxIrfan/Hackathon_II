"""AI Agent initialization using OpenAI Agents SDK with Gemini.

[Task]: T014
[From]: specs/004-ai-chatbot/tasks.md

This module initializes the OpenAI Agents SDK with Gemini models via AsyncOpenAI adapter.
It provides the task management agent that can interact with MCP tools to perform
task operations on behalf of users.
"""
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from typing import Optional, Any
import logging
import json # Added json


from core.config import get_settings
from ..mcp.todo_tools import create_todo, read_todos, update_todo, delete_todo

logger = logging.getLogger(__name__)
settings = get_settings()


# Initialize AsyncOpenAI client configured for Gemini API
# [From]: specs/004-ai-chatbot/plan.md - Technical Context
# [From]: specs/004-ai-chatbot/tasks.md - Implementation Notes
_gemini_client: Optional[AsyncOpenAI] = None


def get_gemini_client() -> AsyncOpenAI:
    """Get or create the AsyncOpenAI client for Gemini API.

    [From]: specs/004-ai-chatbot/plan.md - Gemini Integration Pattern

    The client uses Gemini's OpenAI-compatible endpoint:
    https://generativelanguage.googleapis.com/v1beta/openai/

    Returns:
        AsyncOpenAI: Configured client for Gemini API

    Raises:
        ValueError: If GEMINI_API_KEY is not configured
    """
    global _gemini_client

    if _gemini_client is None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Please set GEMINI_API_KEY in your environment variables."
            )

        _gemini_client = AsyncOpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=settings.GEMINI_API_KEY
        )
        logger.info("✅ Gemini AI client initialized via AsyncOpenAI adapter")

    return _gemini_client


# Helper method to define tools
TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "create_todo",
            "description": "Create a new todo task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the task"},
                    "description": {"type": "string", "description": "Description of the task"},
                    "user_id": {"type": "string", "description": "User ID"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_todos",
            "description": "Read and list todos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "filters": {
                        "type": "object",
                        "description": "Filters e.g. {'completed': true}",
                        "properties": {
                            "completed": {"type": "boolean"}
                        }
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_todo",
            "description": "Update an existing todo task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {"type": "string", "description": "ID of the todo to update"},
                    "updates": {
                        "type": "object",
                        "description": "Fields to update e.g. {'completed': true, 'title': 'New Title'}",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "completed": {"type": "boolean"}
                        }
                    }
                },
                "required": ["todo_id", "updates"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo",
            "description": "Delete a todo task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {"type": "string", "description": "ID of the todo to delete"}
                },
                "required": ["todo_id"]
            }
        }
    }
]

# Initialize the task management agent
# [From]: specs/004-ai-chatbot/spec.md - US1
_task_agent: Optional[Agent] = None


def get_task_agent() -> Agent:
    """Get or create the task management AI agent.

    [From]: specs/004-ai-chatbot/plan.md - AI Agent Layer

    The agent is configured to:
    - Help users create, list, update, complete, and delete tasks
    - Understand natural language requests
    - Ask for clarification when requests are ambiguous
    - Confirm actions clearly

    Returns:
        Agent: Configured task management agent

    Raises:
        ValueError: If GEMINI_API_KEY is not configured
    """
    global _task_agent

    if _task_agent is None:
        gemini_client = get_gemini_client()

        # Initialize task management agent
        _task_agent = Agent(
            name="task_manager",
            instructions="""You are a helpful task management assistant.

Users can create, list, update, complete, and delete tasks through natural language.

Your capabilities:
- Create tasks with title, description, due date, and priority
- List and filter tasks (e.g., "show me high priority tasks due this week")
- Update existing tasks (title, description, due date, priority)
- Mark tasks as complete or incomplete
- Delete tasks

Guidelines:
- Always confirm actions clearly before executing them
- Ask for clarification when requests are ambiguous
- Be concise and friendly in your responses
- Use the MCP tools provided to interact with the user's task list
- Maintain context across the conversation
- If you need more information (e.g., which task to update), ask specifically

Empty task list handling:
- [From]: T026 - When users have no tasks, respond warmly and offer to help create one
- Examples: "You don't have any tasks yet. Would you like me to help you create one?"
- For filtered queries with no results: "No tasks match that criteria. Would you like to see all your tasks instead?"

Task presentation:
- When listing tasks, organize them logically (e.g., pending first, then completed)
- Include key details: title, due date, priority, completion status
- Use clear formatting (bullet points or numbered lists)
- For long lists, offer to filter or show specific categories

Example interactions:
User: "Create a task to buy groceries"
You: "I'll create a task titled 'Buy groceries' for you." → Use create_todo tool

User: "Show me my tasks"
You: "Let me get your task list." → Use read_todos tool

User: "What are my pending tasks?"
You: "Let me check your pending tasks." → Use read_todos tool with filters={'completed': False}

User: "I have no tasks"
You: "That's right! You don't have any tasks yet. Would you like me to help you create one?"

User: "Mark the grocery task as complete"
You: "Which task would you like me to mark as complete?" → Ask for clarification if unclear

User: "I need to finish the report by Friday"
You: "I'll create a task 'Finish the report' due this Friday." → Use create_todo with due_date
""",
            model=OpenAIChatCompletionsModel(
                model=settings.GEMINI_MODEL,
                openai_client=gemini_client,
            ),
            tools=[create_todo, read_todos, update_todo, delete_todo],
        )
        logger.info(f"✅ Task agent initialized with model: {settings.GEMINI_MODEL}")

    return _task_agent


class TodoAgent:
    """Task management AI agent.

    This class provides methods to process natural language requests related to
    task management using the OpenAI Agents SDK with Gemini.
    """

    def __init__(self):
        self._gemini_client = get_gemini_client()

    async def process_request(
        self,
        user_input: str,
        user_id: str,
        session: Any = None,
        conversation_history: Optional[list[dict[str, str]]] = None
    ) -> dict[str, Any]:
        """Process a natural language request.

        Args:
            user_input: The user's query
            user_id: User identification for tool context
            session: Optional database session
            conversation_history: List of previous messages

        Returns:
            dict: Response containing 'response', 'tool_calls', and 'tool_results'
        """
        try:
            # Prepare messages: history + current input
            messages = []
            
            # System prompt
            system_prompt = f"""You are a helpful task management assistant.
Current User ID: {user_id}
Always include user_id="{user_id}" when calling tools that require it.

Capabilities:
- Create, Read, Update, Delete tasks
- Filter tasks

When starting, try to be helpful and check for existing tasks if the user asks broad questions.
"""
            messages.append({"role": "system", "content": system_prompt})

            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": user_input})

            logger.info(f"🚀 Running agent for user {user_id}: {user_input[:50]}...")
            
            # First LLM call
            response = await self._gemini_client.chat.completions.create(
                model=settings.GEMINI_MODEL,
                messages=messages,
                tools=TOOLS_DEFINITION,
                tool_choice="auto"
            )
            
            assistant_msg = response.choices[0].message
            tool_calls = assistant_msg.tool_calls
            tool_results = []
            tool_call_info = [] # For API response
            final_response_text = assistant_msg.content

            if tool_calls:
                logger.info(f"🛠️ Agent requested {len(tool_calls)} tool calls")
                
                # Execute tools
                for tc in tool_calls:
                    fn_name = tc.function.name
                    args_str = tc.function.arguments
                    try:
                        args = json.loads(args_str)
                    except json.JSONDecodeError:
                        logger.error(f"Failed to parse arguments: {args_str}")
                        args = {}
                    
                    # Ensure user_id is in args if valid parameter for the function
                    # Check our tools definition or just add it if missing and safe
                    if "user_id" not in args and fn_name in ["create_todo", "read_todos"]:
                         args["user_id"] = user_id

                    result = None
                    try:
                        if fn_name == "create_todo":
                            result = await create_todo(**args)
                        elif fn_name == "read_todos":
                            result = await read_todos(**args)
                        elif fn_name == "update_todo":
                            result = await update_todo(**args)
                        elif fn_name == "delete_todo":
                            result = await delete_todo(**args)
                        else:
                            result = {"error": f"Unknown tool: {fn_name}"}
                    except Exception as tool_err:
                        logger.error(f"Tool execution error {fn_name}: {tool_err}")
                        result = {"error": str(tool_err)}
                    
                    tool_results.append({
                        "tool_call_id": tc.id,
                        "role": "tool",
                        "name": fn_name,
                        "content": json.dumps(result, default=str)
                    })
                    
                    tool_call_info.append({
                        "name": fn_name,
                        "arguments": args_str
                    })

                # Second LLM call with tool results
                messages.append(assistant_msg) # Add assistant's tool request
                messages.extend(tool_results)  # Add tool outputs
                
                final_response = await self._gemini_client.chat.completions.create(
                    model=settings.GEMINI_MODEL,
                    messages=messages
                )
                final_response_text = final_response.choices[0].message.content

            logger.info(f"✅ Agent processed request successfully for user {user_id}")
            return {
                "response": final_response_text,
                "tool_calls": tool_call_info,
                "tool_results": [json.loads(tr["content"]) for tr in tool_results]
            }

        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"❌ Error in TodoAgent.process_request: {e}\n{error_trace}")
            
            error_msg = str(e).lower()
            if "api_key" in error_msg:
                return {
                    "response": "I'm sorry, but there's a problem with my AI service configuration (API key issue). Please contact support.",
                    "tool_calls": [],
                    "tool_results": []
                }
            elif "429" in error_msg or "rate limit" in error_msg or "quota" in error_msg:
                return {
                    "response": "I'm sorry, but I've reached my message limit for now (Gemini API 429 Rate Limit). Please try again in a few moments.",
                    "tool_calls": [],
                    "tool_results": []
                }
            else:
                return {
                    "response": f"I encountered an error while processing your request: {str(e)}",
                    "tool_calls": [],
                    "tool_results": []
                }


def is_gemini_configured() -> bool:
    """Check if Gemini API is properly configured."""
    return bool(settings.GEMINI_API_KEY)


async def run_agent(
    messages: list[dict[str, str]],
    user_id: str,
    context: Optional[dict] = None
) -> str:
    """Helper function for backward compatibility and streaming."""
    agent = TodoAgent()
    result = await agent.process_request(
        user_input=messages[-1]["content"] if messages else "",
        user_id=user_id,
        conversation_history=messages[:-1] if messages else []
    )
    return result["response"]


__all__ = [
    "get_gemini_client",
    "get_task_agent",
    "run_agent",
    "is_gemini_configured",
    "TodoAgent"
]