"""
Simple FastAPI server for PMM Deep Agent.
Runs without Docker or LangSmith.
"""

import os
import json
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from .prompts import MAIN_SYSTEM_PROMPT
from .tools import ALL_TOOLS

app = FastAPI(title="PMM Deep Agent", version="0.1.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model with tools
llm = ChatAnthropic(
    model_name=os.getenv("MODEL", "claude-sonnet-4-20250514"),
    max_tokens=8192,
)
llm_with_tools = llm.bind_tools(ALL_TOOLS)

# Simple in-memory session storage
sessions: dict = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_calls: list | None = None


@app.get("/health")
def health():
    return {"status": "ok", "agent": "pmm-deep-agent"}


@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Simple chat endpoint."""
    session_id = request.session_id or str(uuid.uuid4())

    # Get or create session
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [
                {"role": "system", "content": MAIN_SYSTEM_PROMPT}
            ]
        }

    session = sessions[session_id]
    session["messages"].append({"role": "user", "content": request.message})

    # Call Claude
    messages = [
        HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
        for m in session["messages"] if m["role"] != "system"
    ]

    response = await llm_with_tools.ainvoke(
        [{"role": "system", "content": MAIN_SYSTEM_PROMPT}] + messages
    )

    # Extract response
    response_text = response.content if isinstance(response.content, str) else ""
    tool_calls = None

    if hasattr(response, 'tool_calls') and response.tool_calls:
        tool_calls = [
            {"name": tc["name"], "args": tc["args"]}
            for tc in response.tool_calls
        ]
        # For tool calls, format as text
        if not response_text:
            response_text = f"Using tools: {', '.join(tc['name'] for tc in tool_calls)}"

    session["messages"].append({"role": "assistant", "content": response_text})

    return ChatResponse(
        session_id=session_id,
        response=response_text,
        tool_calls=tool_calls
    )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint."""
    session_id = request.session_id or str(uuid.uuid4())

    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [
                {"role": "system", "content": MAIN_SYSTEM_PROMPT}
            ]
        }

    session = sessions[session_id]
    session["messages"].append({"role": "user", "content": request.message})

    async def generate() -> AsyncGenerator[str, None]:
        messages = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in session["messages"] if m["role"] != "system"
        ]

        full_response = ""

        async for chunk in llm_with_tools.astream(
            [{"role": "system", "content": MAIN_SYSTEM_PROMPT}] + messages
        ):
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                if isinstance(content, str):
                    full_response += content
                    yield f"data: {json.dumps({'type': 'text', 'content': content})}\n\n"
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                full_response += item.get('text', '')
                                yield f"data: {json.dumps({'type': 'text', 'content': item.get('text', '')})}\n\n"
                            elif item.get('type') == 'tool_use':
                                yield f"data: {json.dumps({'type': 'tool_call', 'name': item.get('name'), 'args': item.get('input', {})})}\n\n"

            if hasattr(chunk, 'tool_calls') and chunk.tool_calls:
                for tc in chunk.tool_calls:
                    yield f"data: {json.dumps({'type': 'tool_call', 'name': tc.get('name'), 'args': tc.get('args', {})})}\n\n"

        session["messages"].append({"role": "assistant", "content": full_response})
        yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """Clear a session."""
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Session not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8123)
