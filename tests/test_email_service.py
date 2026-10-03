import smtplib
from unittest.mock import MagicMock, patch

import pytest

from services.email_service import (
    EmailConfig,
    EmailDeliveryError,
    build_care_plan_message,
    send_care_plan,
)

CONFIG = EmailConfig(sender_address="sender@gmail.com", app_password="abcdabcdabcdabcd")


def test_message_contents():
    msg = build_care_plan_message("sender@gmail.com", "me@x.com", "Ravi", "1. Water less")
    assert msg["To"] == "me@x.com"
    assert "Hi Ravi" in msg.get_content()
    assert "1. Water less" in msg.get_content()


@patch("services.email_service.smtplib.SMTP_SSL")
def test_send_logs_in_and_sends(mock_smtp):
    server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = server
    send_care_plan(CONFIG, "me@x.com", "Ravi", "plan")
    server.login.assert_called_once_with("sender@gmail.com", "abcdabcdabcdabcd")
    server.send_message.assert_called_once()


@patch("services.email_service.smtplib.SMTP_SSL")
def test_auth_failure_has_friendly_message(mock_smtp):
    mock_smtp.return_value.__enter__.return_value.login.side_effect = smtplib.SMTPAuthenticationError(535, b"bad")
    with pytest.raises(EmailDeliveryError, match="App Password"):
        send_care_plan(CONFIG, "me@x.com", "Ravi", "plan")
