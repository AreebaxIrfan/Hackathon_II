from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
import json
from datetime import datetime

from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate, ConversationRead
from ..models.message import Message, MessageCreate, MessageUpdate, MessageRead
from ..models.tool_call import ToolCall, ToolCallCreate, ToolCallUpdate, ToolCallRead


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, conversation_create: ConversationCreate) -> ConversationRead:
        """Create a new conversation."""
        conversation = Conversation.from_orm(conversation_create)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)

        return ConversationRead.from_orm(conversation)

    async def get_conversation_by_id(self, conversation_id: int, user_id: str) -> Conversation:
        """Get a conversation by ID, ensuring it belongs to the user."""
        statement = select(Conversation).where(Conversation.id == conversation_id).where(Conversation.user_id == user_id)
        result = await self.session.exec(statement)
        conversation = result.first()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation

    async def get_conversations_for_user(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        result = await self.session.exec(statement)
        return result.all()

    async def add_message_to_conversation(self, conversation_id: int, user_id: str, message_create: MessageCreate) -> Message:
        """Add a message to a conversation, ensuring the user owns the conversation."""
        # Verify the conversation belongs to the user
        await self.get_conversation_by_id(conversation_id, user_id)

        message = Message.from_orm(message_create)
        message.conversation_id = conversation_id
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)

        return message

    async def get_messages_for_conversation(self, conversation_id: int, user_id: str) -> List[Message]:
        """Get all messages for a conversation, ensuring the user owns the conversation."""
        # Verify the conversation belongs to the user
        await self.get_conversation_by_id(conversation_id, user_id)

        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        result = await self.session.exec(statement)
        return result.all()

    async def get_conversation_history(self, conversation_id: int, user_id: str, limit: int = 50) -> List[Message]:
        """Get conversation history with optional limit."""
        # Verify the conversation belongs to the user
        await self.get_conversation_by_id(conversation_id, user_id)

        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await self.session.exec(statement)
        messages = result.all()

        # Return in chronological order (oldest first)
        return list(reversed(messages))

    async def add_tool_call_to_conversation(self, conversation_id: int, user_id: str, tool_call_create: ToolCallCreate) -> ToolCall:
        """Add a tool call to a conversation, ensuring the user owns the conversation."""
        # Verify the conversation belongs to the user
        await self.get_conversation_by_id(conversation_id, user_id)

        tool_call = ToolCall.from_orm(tool_call_create)
        tool_call.conversation_id = conversation_id
        self.session.add(tool_call)
        await self.session.commit()
        await self.session.refresh(tool_call)

        return tool_call

    async def get_tool_calls_for_conversation(self, conversation_id: int, user_id: str) -> List[ToolCall]:
        """Get all tool calls for a conversation, ensuring the user owns the conversation."""
        # Verify the conversation belongs to the user
        await self.get_conversation_by_id(conversation_id, user_id)

        statement = select(ToolCall).where(ToolCall.conversation_id == conversation_id).order_by(ToolCall.created_at.asc())
        result = await self.session.exec(statement)
        return result.all()