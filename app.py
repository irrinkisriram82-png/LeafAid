"""LeafAid - an AI plant doctor. Streamlit UI entry point.

Run with:  streamlit run app.py
"""
from __future__ import annotations

import logging
from typing import Optional

import streamlit as st

from config import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_BYTES, Settings, load_settings
from prompts import (
    DEFAULT_PHOTO_PROMPT,
    LANDING_FEATURES,
    QUICK_CHECKS,
    SUMMARY_REQUEST_PROMPT,
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
)
from services.email_service import EmailDeliveryError, send_care_plan
from services.gemini_service import (
    GeminiError,
    build_parts,
    create_chat,
    create_client,
    send_message,
)
from services.validators import clean_name, is_valid_email
from ui import components
from ui.styles import CSS

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

st.set_page_config(page_title="LeafAid - AI Plant Clinic", page_icon="🌿", layout="centered")


def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


@st.cache_resource
def get_gemini_client(api_key: str):
    """One shared client; Streamlit reruns the script on every interaction."""
    return create_client(api_key)


# ---------- session + chat helpers ----------

def start_conversation(settings: Settings) -> None:
    client = get_gemini_client(settings.gemini_api_key)
    st.session_state.chat = create_chat(client, settings.gemini_model, SYSTEM_PROMPT)
    st.session_state.messages = []
    st.session_state.analysis_count = 0
    st.session_state.photo_count = 0


def render_message(message: dict) -> None:
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        else:
            st.image(message["content"])


def add_message(role: str, kind: str, content) -> None:
    """Save a message to history and draw it immediately."""
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])


# ---------- landing / onboarding ----------

def render_onboarding(settings: Settings) -> None:
    left, right = st.columns([6, 5], gap="large")
    with left:
        html(components.landing_hero(LANDING_FEATURES))
    with right:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        with st.form("onboarding_form"):
            st.subheader("Start your consultation")
            name = st.text_input("Your name")
            email = st.text_input(
                "Your email address",
                placeholder="you@example.com",
                help="LeafAid will send your care plan here.",
            )
            submitted = st.form_submit_button("Open my plant clinic 🚀", use_container_width=True)

    if not submitted:
        return
    if not name.strip() or not email.strip():
        st.warning("Please fill in both your name and email address.")
    elif not is_valid_email(email):
        st.warning("That email address doesn't look right. Please check it.")
    else:
        st.session_state.name = clean_name(name)
        st.session_state.email = email.strip()
        st.session_state.emails_sent = 0
        start_conversation(settings)
        st.session_state.onboarded = True
        st.rerun()


# ---------- dashboard actions ----------

def handle_turn(text: str, image_bytes: Optional[bytes], mime_type: Optional[str]) -> None:
    """Send one user turn (text and/or photo) to Gemini and show the reply."""
    text = (text or "").strip()
    if not text and image_bytes is None:
        return
    if image_bytes is not None and len(image_bytes) > MAX_UPLOAD_BYTES:
        st.warning("That photo is larger than 5 MB. Please upload a smaller one.")
        return

    if image_bytes is not None:
        add_message("user", "image", image_bytes)
    if text:
        add_message("user", "text", text)

    parts = build_parts(text, image_bytes, mime_type, DEFAULT_PHOTO_PROMPT)
    with st.spinner("Examining your plant..."):
        try:
            answer = send_message(st.session_state.chat, parts)
        except GeminiError as error:
            st.error(f"Sorry, LeafAid couldn't answer that: {error}")
            return
    add_message("assistant", "text", answer)
    st.session_state.analysis_count += 1
    if image_bytes is not None:
        st.session_state.photo_count += 1


def handle_email_click(settings: Settings, status) -> None:
    """Ask Gemini for a care plan, then email it."""
    with st.spinner("Writing and sending your care plan..."):
        try:
            plan = send_message(st.session_state.chat, [SUMMARY_REQUEST_PROMPT])
            send_care_plan(settings.email, st.session_state.email, st.session_state.name, plan)
        except (GeminiError, EmailDeliveryError) as error:
            status.error(f"Couldn't send that: {error}")
        else:
            st.session_state.emails_sent += 1
            status.success("Sent! Check your inbox (and spam folder) 📬")


# ---------- sidebar ----------

def render_sidebar_top() -> Optional[str]:
    """Profile + quick health checks. Returns the prompt of a clicked check, if any."""
    chosen = None
    with st.sidebar:
        html(components.sidebar_brand())
        html(components.profile_card(st.session_state.name, st.session_state.email))
        html(components.section_label("Quick health checks"))
        for index, (icon, title, prompt) in enumerate(QUICK_CHECKS):
            if st.button(f"{icon}  {title}", key=f"quick_{index}", use_container_width=True):
                chosen = prompt
    return chosen


def render_sidebar_actions(settings: Settings) -> bool:
    """Email + new-consultation buttons. Returns True if the email button was clicked."""
    with st.sidebar:
        html(components.section_label("Actions"))
        email_clicked = st.button(
            "📤  Email my care plan",
            type="primary",
            disabled=st.session_state.analysis_count == 0,
            use_container_width=True,
        )
        if st.button("➕  New consultation", use_container_width=True):
            start_conversation(settings)
            st.rerun()
        html(components.tip_box())
    return email_clicked


# ---------- dashboard ----------

def render_dashboard(settings: Settings) -> None:
    quick_prompt = render_sidebar_top()

    html(components.hero_banner(st.session_state.name))
    stats_slot = st.empty()
    status = st.empty()

    if not st.session_state.messages:
        add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
    else:
        for message in st.session_state.messages:
            render_message(message)

    user_input = st.chat_input(
        "Describe your plant's problem, or attach a photo",
        accept_file=True,
        file_type=ALLOWED_IMAGE_TYPES,
    )

    if quick_prompt:
        handle_turn(quick_prompt, None, None)
    elif user_input:
        photo = user_input.files[0] if user_input.files else None
        handle_turn(
            user_input.text,
            photo.getvalue() if photo else None,
            photo.type if photo else None,
        )

    # Drawn after processing so button state and stats reflect the newest reply.
    if render_sidebar_actions(settings):
        handle_email_click(settings, status)

    stats_slot.markdown(
        components.stats_row(
            st.session_state.analysis_count,
            st.session_state.photo_count,
            st.session_state.emails_sent,
        ),
        unsafe_allow_html=True,
    )


def main() -> None:
    html(f"<style>{CSS}</style>")
    settings = load_settings()
    if "onboarded" not in st.session_state:
        render_onboarding(settings)
        st.stop()
    render_dashboard(settings)


main()
