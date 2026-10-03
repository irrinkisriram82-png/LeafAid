"""Send care-plan emails through Gmail SMTP."""
from __future__ import annotations

import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_TIMEOUT_SECONDS = 15
SUBJECT = "Your LeafAid plant care plan 🌿"
FOOTER = "- LeafAid 🌿\nPhoto diagnoses are estimates. For serious problems, visit a local nursery."


class EmailDeliveryError(Exception):
    """Raised with a user-friendly message when an email cannot be sent."""


@dataclass(frozen=True)
class EmailConfig:
    sender_address: str
    app_password: str


def build_care_plan_message(sender: str, recipient: str, user_name: str, body: str) -> EmailMessage:
    """Create the email (UTF-8, header-injection safe)."""
    message = EmailMessage()
    message["Subject"] = SUBJECT
    message["From"] = f"LeafAid <{sender}>"
    message["To"] = recipient
    message.set_content(f"Hi {user_name},\n\n{body.strip()}\n\n{FOOTER}")
    return message


def send_care_plan(config: EmailConfig, recipient: str, user_name: str, body: str) -> None:
    """Send the care plan. Raises EmailDeliveryError on any failure."""
    try:
        message = build_care_plan_message(config.sender_address, recipient, user_name, body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS, context=context) as server:
            server.login(config.sender_address, config.app_password)
            server.send_message(message)
    except smtplib.SMTPAuthenticationError as error:
        logger.error("Gmail authentication failed")
        raise EmailDeliveryError(
            "Gmail rejected the login. Check GMAIL_ADDRESS and use a 16-character App Password."
        ) from error
    except smtplib.SMTPRecipientsRefused as error:
        raise EmailDeliveryError("That email address was rejected. Please check it.") from error
    except (smtplib.SMTPException, OSError, ValueError) as error:
        logger.exception("Email delivery failed")
        raise EmailDeliveryError(f"Could not send the email: {error}") from error
