import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import get_session
from ...task_agents.todo_agent import TodoAgent
from ...services.conversation_service import ConversationService
from ...models.conversation import ConversationCreate
from ...models.message import MessageCreate
from ...models.tool_call import ToolCallCreate
from ...schemas.chat_schemas import ChatRequest


router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.get("/{user_id}/conversations")
async def get_conversations(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    conversation_service = ConversationService(session)
    conversations = await conversation_service.get_conversations_for_user(user_uuid)
    return conversations


@router.get("/{user_id}/conversations/{conversation_id}/history")
async def get_history(
    user_id: str,
    conversation_id: str,
    session: AsyncSession = Depends(get_session)
):
    try:
        user_uuid = uuid.UUID(user_id)
        conv_uuid = uuid.UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    conversation_service = ConversationService(session)
    history = await conversation_service.get_conversation_history(conv_uuid, user_uuid)
    return history


@router.post("/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    message = request.message
    conversation_id = request.conversation_id
    
    # Convert string user_id to UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    # Initialize the AI agent
    agent = TodoAgent()

    # Get conversation service
    conversation_service = ConversationService(session)

    # Get conversation history if conversation_id is provided
    conversation_history = None
    if conversation_id:
        try:
            conv_uuid = uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation ID format")

        # Get the conversation history
        conv_history = await conversation_service.get_conversation_history(conv_uuid, user_uuid)

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
        conversation_create = ConversationCreate(user_id=user_uuid)
        conversation = await conversation_service.create_conversation(conversation_create)
        conv_uuid = conversation.id
        conversation_id = str(conv_uuid)

    try:
        # Process the user's request with the AI agent
        result = await agent.process_request(
            user_input=message,
            user_id=user_id, # agent.process_request takes string and converts internally
            session=session,
            conversation_history=conversation_history
        )

        # Save the user's message to the conversation
        message_create = MessageCreate(
            user_id=user_uuid,
            conversation_id=conv_uuid,
            role="user",
            content=message
        )
        await conversation_service.add_message_to_conversation(
            conversation_id=conv_uuid,
            user_id=user_uuid,
            message_create=message_create
        )

        # Save the agent's response to the conversation
        if result.get("response"):
            response_message_create = MessageCreate(
                user_id=user_uuid,
                conversation_id=conv_uuid,
                role="assistant",
                content=result["response"]
            )
            await conversation_service.add_message_to_conversation(
                conversation_id=conv_uuid,
                user_id=user_uuid,
                message_create=response_message_create
            )

        # Save any tool calls that were made
        if result.get("tool_calls"):
            for i, tool_call in enumerate(result["tool_calls"]):
                tool_call_create = ToolCallCreate(
                    conversation_id=conv_uuid,
                    tool_name=tool_call["name"],
                    arguments=str(tool_call["arguments"]),  # Convert to string for storage
                    result=str(result["tool_results"][i]) if result.get("tool_results") else None
                )
                await conversation_service.add_tool_call_to_conversation(
                    conversation_id=conv_uuid,
                    user_id=user_uuid,
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