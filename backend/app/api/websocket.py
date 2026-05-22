from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

import traceback
import uuid

from app.agents.conversation_agent import process_message

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    session_id = str(uuid.uuid4())

    print("Connected:", session_id)

    try:

        while True:

            data = await websocket.receive_text()

            result = await process_message(
                session_id,
                data
            )

            await websocket.send_json(result)

    except WebSocketDisconnect:

        print("Disconnected")

    except Exception:

        traceback.print_exc()