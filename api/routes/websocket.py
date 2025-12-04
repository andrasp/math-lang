"""WebSocket endpoint for real-time evaluation."""

import json
import time
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.sessions import session_manager

router = APIRouter()


class WebSocketProtocol:
    """Protocol for WebSocket messages."""

    EVALUATE = "evaluate"
    CANCEL = "cancel"
    RESULT = "result"
    ERROR = "error"
    COMPLETE = "complete"


async def send_json(websocket: WebSocket, message: dict[str, Any]) -> None:
    """Send JSON message to client."""
    await websocket.send_text(json.dumps(message))


async def send_result(
    websocket: WebSocket,
    value: str,
    type_name: str,
    is_assignment: bool = False,
    variable_name: str | None = None,
    elapsed_ms: float = 0,
    image_data: str | None = None,
) -> None:
    """Send evaluation result to client."""
    message = {
        "type": WebSocketProtocol.RESULT,
        "value": value,
        "type_name": type_name,
        "is_assignment": is_assignment,
        "variable_name": variable_name,
        "elapsed_ms": elapsed_ms,
    }
    if image_data:
        message["image_data"] = image_data
    await send_json(websocket, message)


async def send_error(websocket: WebSocket, message: str, line: int | None = None, column: int | None = None) -> None:
    """Send error to client."""
    await send_json(
        websocket,
        {
            "type": WebSocketProtocol.ERROR,
            "message": message,
            "line": line,
            "column": column,
        },
    )


async def send_complete(websocket: WebSocket, variables: dict[str, dict[str, str]]) -> None:
    """Send completion message with final variables state."""
    await send_json(
        websocket,
        {
            "type": WebSocketProtocol.COMPLETE,
            "variables": variables,
        },
    )


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str) -> None:
    """WebSocket endpoint for real-time evaluation.

    Protocol:
    - Client sends: {"type": "evaluate", "source": "..."}
    - Server responds with multiple messages:
      - {"type": "result", "value": "...", "type_name": "...", ...} for each result
      - {"type": "error", "message": "...", ...} on error
      - {"type": "complete", "variables": {...}} when done
    """
    await websocket.accept()
    session_info = session_manager.get_or_create(session_id if session_id != "new" else None)

    await send_json(
        websocket,
        {
            "type": "connected",
            "session_id": session_info.id,
            "variables": session_info.get_variables(),
        },
    )

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await send_error(websocket, "Invalid JSON")
                continue

            msg_type = message.get("type")

            if msg_type == WebSocketProtocol.EVALUATE:
                source = message.get("source", "")
                await handle_evaluate(websocket, session_info, source)
            elif msg_type == WebSocketProtocol.CANCEL:
                pass
            else:
                await send_error(websocket, f"Unknown message type: {msg_type}")

    except WebSocketDisconnect:
        pass


async def handle_evaluate(websocket: WebSocket, session_info: Any, source: str) -> None:
    """Handle evaluation request."""
    from mathlang.engine import evaluate
    from api.plotting import render_plot

    start_time = time.time()

    try:
        results = evaluate(source, session_info.session)

        for r in results:
            elapsed_ms = (time.time() - start_time) * 1000
            # Check if result is a plot type and render it
            image_data = render_plot(r.value) if r.value else None
            await send_result(
                websocket,
                value=r.value.display() if r.value else "",
                type_name=r.value.type_name if r.value else "",
                is_assignment=r.is_assignment,
                variable_name=r.variable_name,
                elapsed_ms=elapsed_ms,
                image_data=image_data,
            )

        await send_complete(websocket, session_info.get_variables())

    except Exception as e:
        await send_error(websocket, str(e))
        await send_complete(websocket, session_info.get_variables())
