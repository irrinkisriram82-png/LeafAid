from unittest.mock import MagicMock

import pytest

from services.gemini_service import GeminiError, build_parts, send_message


def test_text_only():
    assert build_parts("hello", None, None, "default") == ["hello"]


def test_photo_without_text_uses_default_prompt():
    parts = build_parts("", b"123", "image/png", "default")
    assert len(parts) == 2 and parts[1] == "default"


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        build_parts("", None, None, "default")


def test_send_message_returns_text():
    chat = MagicMock()
    chat.send_message.return_value.text = " hi "
    assert send_message(chat, ["x"]) == "hi"


def test_send_message_wraps_sdk_errors():
    chat = MagicMock()
    chat.send_message.side_effect = RuntimeError("boom")
    with pytest.raises(GeminiError):
        send_message(chat, ["x"])


def test_empty_response_is_error():
    chat = MagicMock()
    chat.send_message.return_value.text = None
    with pytest.raises(GeminiError):
        send_message(chat, ["x"])
