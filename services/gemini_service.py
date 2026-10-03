"""Thin wrapper around the Google Gemini SDK (chat + vision)."""
from __future__ import annotations

import logging
from typing import Any, List, Optional

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class GeminiError(Exception):
    """Raised when Gemini fails or returns no usable answer."""


def create_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def create_chat(client: genai.Client, model: str, system_prompt: str) -> Any:
    """Start a conversation that remembers history and follows ``system_prompt``."""
    return client.chats.create(
        model=model,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )


def build_parts(
    text: str,
    image_bytes: Optional[bytes],
    mime_type: Optional[str],
    default_photo_prompt: str,
) -> List[Any]:
    """Build the message parts for one user turn (optional photo + optional text)."""
    parts: List[Any] = []
    if image_bytes:
        parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type or "image/jpeg"))
    if text:
        parts.append(text)
    elif image_bytes:
        parts.append(default_photo_prompt)
    if not parts:
        raise ValueError("A message needs text, a photo, or both.")
    return parts


def send_message(chat: Any, parts: List[Any]) -> str:
    """Send one turn and return the reply text, or raise GeminiError."""
    try:
        response = chat.send_message(parts)
    except Exception as error:  # SDK raises many error types
        logger.exception("Gemini request failed")
        raise GeminiError(str(error)) from error

    answer = (response.text or "").strip()
    if not answer:
        raise GeminiError("Gemini returned an empty response. Please try again.")
    return answer
