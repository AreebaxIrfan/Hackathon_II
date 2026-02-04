import json
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from pydantic_settings import BaseSettings
from ..services.conversation_service import ConversationService
from ..models.message import MessageCreate


class Settings(BaseSettings):
    openai_api_key: str
    mcp_server_url: str = "http://localhost:8001"

    class Config:
        env_file = ".env"


class TodoAgent:
    def __init__(self):
        self.settings = Settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key)

        # Define the tools available to the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "status": {"type": "string", "description": "Filter by status: all, pending, completed"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task (optional)"},
                            "description": {"type": "string", "description": "New description for the task (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    async def process_request(self, user_input: str, user_id: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Process a natural language request from the user and return a response.

        Args:
            user_input: Natural language input from the user
            user_id: ID of the requesting user
            conversation_history: Previous conversation messages

        Returns:
            Dictionary with response and any tool calls made
        """
        # Prepare the messages for the AI
        messages = []

        if conversation_history:
            # Add conversation history to messages
            for msg in conversation_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": user_input})

        try:
            # Call the OpenAI API with function calling enabled
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Using a model that supports function calling
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            result = {
                "response": "",
                "tool_calls": [],
                "tool_results": []
            }

            if tool_calls:
                # Process each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add user_id if not present in the arguments
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    result["tool_calls"].append({
                        "name": function_name,
                        "arguments": function_args
                    })

                    # In a real implementation, we would call the actual MCP tools
                    # For now, we'll simulate the responses based on the function
                    tool_result = await self._simulate_tool_call(function_name, function_args)
                    result["tool_results"].append(tool_result)

                # Generate a final response based on the tool results
                messages.append(response_message)
                for i, tool_result in enumerate(result["tool_results"]):
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result),
                        "tool_call_id": tool_calls[i].id
                    })

                # Get the final response from the AI based on tool results
                final_response = await self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=messages
                )

                result["response"] = final_response.choices[0].message.content

            else:
                # If no tool calls were made, just return the AI's response
                result["response"] = response_message.content or ""

            return result

        except Exception as e:
            # Handle any errors gracefully
            return {
                "response": "I'm sorry, I encountered an error while processing your request. Could you please try again?",
                "tool_calls": [],
                "tool_results": [],
                "error": str(e)
            }

    async def _simulate_tool_call(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate calling an MCP tool. In a real implementation, this would make
        actual calls to the MCP server.
        """
        # This is a simulation - in a real implementation, we would call the actual MCP tools
        # For now, return appropriate responses based on the function

        if function_name == "add_task":
            return {
                "task_id": 1,  # Simulated task ID
                "status": "created",
                "title": function_args.get("title", "New Task")
            }
        elif function_name == "list_tasks":
            # Simulated task list
            return {
                "tasks": [
                    {"id": 1, "title": "Sample task", "completed": False},
                    {"id": 2, "title": "Another task", "completed": True}
                ]
            }
        elif function_name == "complete_task":
            return {
                "success": True,
                "task_id": function_args.get("task_id"),
                "status": "completed"
            }
        elif function_name == "delete_task":
            return {
                "success": True,
                "task_id": function_args.get("task_id")
            }
        elif function_name == "update_task":
            return {
                "success": True,
                "task_id": function_args.get("task_id")
            }
        else:
            return {
                "error": f"Unknown function: {function_name}",
                "success": False
            }