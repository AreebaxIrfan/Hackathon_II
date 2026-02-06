from typing import List, Optional
from sqlmodel import Session, select
from backend.src.models.conversation import Conversation, ConversationCreate
from backend.src.models.chat_message import ChatMessage, ChatMessageCreate
from uuid import UUID


class ChatService:
    @staticmethod
    def create_conversation(session: Session, conv_create: ConversationCreate, user_id: UUID) -> Conversation:
        """
        Create a new conversation for a user.
        """
        conversation = Conversation.model_validate(conv_create)
        conversation.user_id = user_id
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: UUID) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    @staticmethod
    def create_message(session: Session, msg_create: ChatMessageCreate) -> ChatMessage:
        """
        Create a new chat message.
        """
        message = ChatMessage.model_validate(msg_create)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_messages_for_conversation(session: Session, conversation_id: UUID) -> List[ChatMessage]:
        """
        Get all messages for a conversation.
        """
        statement = select(ChatMessage).where(ChatMessage.conversation_id == conversation_id)
        return session.exec(statement).all()