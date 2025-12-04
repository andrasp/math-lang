"""Session management for the API."""

import time
import uuid
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

from mathlang.engine.session import Session
from mathlang.types.base import MathObject


@dataclass
class SessionInfo:
    """Information about an active session."""

    id: str
    session: Session
    created_at: float
    last_accessed: float = field(default_factory=time.time)

    def touch(self) -> None:
        """Update last accessed time."""
        self.last_accessed = time.time()

    def get_variables(self) -> dict[str, dict[str, str]]:
        """Get all variables as serializable dict."""
        result = {}
        for name, value in self.session.list_variables().items():
            result[name] = {
                "value": value.display(),
                "type": value.type_name,
            }
        return result


class SessionManager:
    """Manages evaluation sessions with expiration."""

    def __init__(self, ttl_seconds: float = 1800):  # 30 minutes default
        self._sessions: dict[str, SessionInfo] = {}
        self._lock = Lock()
        self._ttl = ttl_seconds

    def create(self) -> SessionInfo:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        now = time.time()
        info = SessionInfo(
            id=session_id,
            session=Session(),
            created_at=now,
            last_accessed=now,
        )
        with self._lock:
            self._cleanup_expired()
            self._sessions[session_id] = info
        return info

    def get(self, session_id: str) -> SessionInfo | None:
        """Get a session by ID, updating last accessed time."""
        with self._lock:
            self._cleanup_expired()
            info = self._sessions.get(session_id)
            if info:
                info.touch()
            return info

    def get_or_create(self, session_id: str | None) -> SessionInfo:
        """Get existing session or create new one."""
        if session_id:
            info = self.get(session_id)
            if info:
                return info
        return self.create()

    def delete(self, session_id: str) -> bool:
        """Delete a session. Returns True if it existed."""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

    def clear(self, session_id: str) -> bool:
        """Clear all variables in a session. Returns True if session exists."""
        with self._lock:
            info = self._sessions.get(session_id)
            if info:
                info.session.clear()
                info.touch()
                return True
            return False

    def list_sessions(self) -> list[dict[str, Any]]:
        """List all active sessions."""
        with self._lock:
            self._cleanup_expired()
            return [
                {
                    "id": info.id,
                    "created_at": info.created_at,
                    "last_accessed": info.last_accessed,
                    "variable_count": len(info.session.list_variables()),
                }
                for info in self._sessions.values()
            ]

    def _cleanup_expired(self) -> None:
        """Remove expired sessions. Must be called with lock held."""
        now = time.time()
        expired = [
            sid
            for sid, info in self._sessions.items()
            if now - info.last_accessed > self._ttl
        ]
        for sid in expired:
            del self._sessions[sid]


# Global session manager instance
session_manager = SessionManager()
