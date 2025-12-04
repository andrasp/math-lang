"""Session management endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.sessions import session_manager

router = APIRouter()


class SessionResponse(BaseModel):
    """Response for session creation/retrieval."""

    session_id: str
    created_at: float
    last_accessed: float
    variables: dict[str, dict[str, str]]


class SessionListItem(BaseModel):
    """Item in session list response."""

    id: str
    created_at: float
    last_accessed: float
    variable_count: int


class SessionListResponse(BaseModel):
    """Response for listing sessions."""

    sessions: list[SessionListItem]


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


@router.post("", response_model=SessionResponse)
async def create_session() -> SessionResponse:
    """Create a new evaluation session."""
    info = session_manager.create()
    return SessionResponse(
        session_id=info.id,
        created_at=info.created_at,
        last_accessed=info.last_accessed,
        variables=info.get_variables(),
    )


@router.get("", response_model=SessionListResponse)
async def list_sessions() -> SessionListResponse:
    """List all active sessions."""
    sessions = session_manager.list_sessions()
    return SessionListResponse(
        sessions=[SessionListItem(**s) for s in sessions]
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str) -> SessionResponse:
    """Get a session by ID."""
    info = session_manager.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(
        session_id=info.id,
        created_at=info.created_at,
        last_accessed=info.last_accessed,
        variables=info.get_variables(),
    )


@router.delete("/{session_id}", response_model=MessageResponse)
async def delete_session(session_id: str) -> MessageResponse:
    """Delete a session."""
    if session_manager.delete(session_id):
        return MessageResponse(message="Session deleted")
    raise HTTPException(status_code=404, detail="Session not found")


@router.post("/{session_id}/clear", response_model=SessionResponse)
async def clear_session(session_id: str) -> SessionResponse:
    """Clear all variables in a session."""
    if not session_manager.clear(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    info = session_manager.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(
        session_id=info.id,
        created_at=info.created_at,
        last_accessed=info.last_accessed,
        variables=info.get_variables(),
    )
