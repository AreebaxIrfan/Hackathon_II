from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import get_session
from ...agents.todo_agent import TodoAgent
from ...services.conversation_service import ConversationService
from ...models.conversation import ConversationCreate
from ...models.message import MessageCreate
from ...models.tool_call import ToolCallCreate


router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/{user_id}/chat")
async def chat(
    user_id: str,
    message: str,
    conversation_id: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    """
    Process natural language input and manage tasks using the AI agent.

    Args:
        user_id: The ID of the user making the request
        message: User's natural language input
        conversation_id: Existing conversation ID (optional)

    Returns:
        Dictionary with response, conversation_id, and tool calls made
    """
    # Initialize the AI agent
    agent = TodoAgent()

    # Get conversation service
    conversation_service = ConversationService(session)

    # Get conversation history if conversation_id is provided
    conversation_history = None
    if conversation_id:
        # Convert string ID to integer for database operations
        conv_id = int(conversation_id)

        # Get the conversation history
        conv_history = await conversation_service.get_conversation_history(conv_id, user_id)

        # Format the history for the AI agent
        formatted_history = []
        for msg in conv_history:
            formatted_history.append({
                "role": msg.role,
                "content": msg.content
            })

        conversation_history = formatted_history
    else:
        # Create a new conversation
        conversation_create = ConversationCreate(user_id=user_id)
        conversation = await conversation_service.create_conversation(conversation_create)
        conversation_id = str(conversation.id)

    try:
        # Process the user's request with the AI agent
        result = await agent.process_request(
            user_input=message,
            user_id=user_id,
            conversation_history=conversation_history
        )

        # Save the user's message to the conversation
        message_create = MessageCreate(
            user_id=user_id,
            conversation_id=int(conversation_id),
            role="user",
            content=message
        )
        await conversation_service.add_message_to_conversation(
            conversation_id=int(conversation_id),
            user_id=user_id,
            message_create=message_create
        )

        # Save the agent's response to the conversation
        if result.get("response"):
            response_message_create = MessageCreate(
                user_id=user_id,
                conversation_id=int(conversation_id),
                role="assistant",
                content=result["response"]
            )
            await conversation_service.add_message_to_conversation(
                conversation_id=int(conversation_id),
                user_id=user_id,
                message_create=response_message_create
            )

        # Save any tool calls that were made
        if result.get("tool_calls"):
            for i, tool_call in enumerate(result["tool_calls"]):
                tool_call_create = ToolCallCreate(
                    conversation_id=int(conversation_id),
                    tool_name=tool_call["name"],
                    arguments=str(tool_call["arguments"]),  # Convert to string for storage
                    result=str(result["tool_results"][i]) if result.get("tool_results") else None
                )
                await conversation_service.add_tool_call_to_conversation(
                    conversation_id=int(conversation_id),
                    user_id=user_id,
                    tool_call_create=tool_call_create
                )

        # Return the response with conversation ID and tool calls
        return {
            "conversation_id": conversation_id,
            "response": result.get("response", ""),
            "tool_calls": result.get("tool_calls", []),
            "tool_results": result.get("tool_results", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")