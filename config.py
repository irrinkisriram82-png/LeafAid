"""Application settings, loaded once from Streamlit secrets."""
from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from services.email_service import EmailConfig

DEFAULT_MODEL = "gemini-3.5-flash"
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
MAX_UPLOAD_BYTES = 5 * 1024 * 1024


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str
    email: EmailConfig


def load_settings() -> Settings:
    """Read secrets; show a helpful error and stop the app if any are missing."""
    try:
        return Settings(
            gemini_api_key=st.secrets["GEMINI_API_KEY"],
            gemini_model=st.secrets.get("GEMINI_MODEL", DEFAULT_MODEL),
            email=EmailConfig(
                sender_address=st.secrets["GMAIL_ADDRESS"],
                # Google displays App Passwords with spaces; strip them.
                app_password=st.secrets["GMAIL_APP_PASSWORD"].replace(" ", ""),
            ),
        )
    except (KeyError, FileNotFoundError) as error:
        st.error(
            "Missing configuration. Copy `.streamlit/secrets.toml.example` to "
            "`.streamlit/secrets.toml` and fill in GEMINI_API_KEY, GMAIL_ADDRESS "
            f"and GMAIL_APP_PASSWORD. ({error})"
        )
        st.stop()
