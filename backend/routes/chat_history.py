from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json
import os

router = APIRouter()

class ChatHistoryItem(BaseModel):
    id: int
    content: str
    timestamp: str
    user_id: Optional[str] = None

class ChatHistoryResponse(BaseModel):
    history: List[ChatHistoryItem]
    total: int

# In-memory storage for demo purposes
# In production, this should be stored in a database
chat_history_storage = [
    {
        "id": 1,
        "content": "What is Tesla's market cap?",
        "timestamp": "2024-01-15T10:30:00Z",
        "user_id": "user1"
    },
    {
        "id": 2,
        "content": "Show me AAPL's Q4 earnings",
        "timestamp": "2024-01-15T11:45:00Z",
        "user_id": "user1"
    },
    {
        "id": 3,
        "content": "Summarize Amazon's 10-K filing",
        "timestamp": "2024-01-15T14:20:00Z",
        "user_id": "user1"
    },
    {
        "id": 4,
        "content": "What are the key risks for Microsoft?",
        "timestamp": "2024-01-16T09:15:00Z",
        "user_id": "user1"
    },
    {
        "id": 5,
        "content": "Compare Google and Apple's revenue growth",
        "timestamp": "2024-01-16T16:30:00Z",
        "user_id": "user1"
    }
]

@router.get("/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
    user_id: Optional[str] = None
):
    """
    Get chat history with optional filtering and pagination
    """
    try:
        # Filter by user_id if provided
        filtered_history = chat_history_storage
        if user_id:
            filtered_history = [chat for chat in chat_history_storage if chat.get("user_id") == user_id]
        
        # Apply pagination
        total = len(filtered_history)
        paginated_history = filtered_history[offset:offset + limit]
        
        return ChatHistoryResponse(
            history=paginated_history,
            total=total
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch chat history: {str(e)}")

@router.post("/chat/history")
async def add_chat_history(item: ChatHistoryItem):
    """
    Add a new chat history item
    """
    try:
        # In production, this would be saved to a database
        chat_history_storage.append(item.dict())
        return {"message": "Chat history item added successfully", "id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add chat history: {str(e)}")

@router.delete("/chat/history/{chat_id}")
async def delete_chat_history(chat_id: int):
    """
    Delete a specific chat history item
    """
    try:
        global chat_history_storage
        original_length = len(chat_history_storage)
        chat_history_storage = [chat for chat in chat_history_storage if chat["id"] != chat_id]
        
        if len(chat_history_storage) == original_length:
            raise HTTPException(status_code=404, detail="Chat history item not found")
        
        return {"message": "Chat history item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete chat history: {str(e)}")

@router.delete("/chat/history")
async def clear_chat_history(user_id: Optional[str] = None):
    """
    Clear all chat history for a user or all users
    """
    try:
        global chat_history_storage
        if user_id:
            original_length = len(chat_history_storage)
            chat_history_storage = [chat for chat in chat_history_storage if chat.get("user_id") != user_id]
            deleted_count = original_length - len(chat_history_storage)
            return {"message": f"Cleared {deleted_count} chat history items for user {user_id}"}
        else:
            deleted_count = len(chat_history_storage)
            chat_history_storage = []
            return {"message": f"Cleared all {deleted_count} chat history items"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear chat history: {str(e)}") 