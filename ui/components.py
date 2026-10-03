"""Pure functions that return HTML snippets (no Streamlit imports, easy to test).

Every user-supplied value is escaped before it is placed in HTML.
"""
from __future__ import annotations

from html import escape
from typing import Sequence, Tuple


def sidebar_brand() -> str:
    return '<div class="la-brand">🌿 Leaf<span>Aid</span></div>'


def section_label(text: str) -> str:
    return f'<div class="la-label">{escape(text)}</div>'


def profile_card(name: str, email: str) -> str:
    initial = escape((name or "?").strip()[:1].upper() or "?")
    return (
        '<div class="la-profile">'
        f'<div class="la-avatar">{initial}</div>'
        f'<div><div class="la-profile-name">{escape(name)}</div>'
        f'<div class="la-profile-email">{escape(email)}</div></div>'
        "</div>"
    )


def tip_box() -> str:
    return (
        '<div class="la-tip">💡 <b>Better photos, better diagnosis:</b> shoot in daylight, '
        "show the affected leaf up close, and include the whole plant in a second shot.</div>"
    )


def hero_banner(name: str) -> str:
    return (
        '<div class="la-hero"><div>'
        '<div class="la-eyebrow">PLANT CLINIC</div>'
        f'<h1 class="la-title">Welcome back, {escape(name)}</h1>'
        "<p>Upload a photo or describe the symptoms. LeafAid will diagnose the problem "
        "and prepare a care plan you can email to yourself.</p>"
        '</div><div class="la-hero-badge">🪴</div></div>'
    )


def _stat(icon: str, value: int, label: str) -> str:
    return (
        '<div class="la-stat">'
        f'<div class="la-stat-icon">{icon}</div>'
        f'<div><div class="la-stat-value">{int(value)}</div>'
        f'<div class="la-stat-label">{escape(label)}</div></div></div>'
    )


def stats_row(consultations: int, photos: int, emails: int) -> str:
    return (
        '<div class="la-stats">'
        + _stat("🩺", consultations, "Consultations")
        + _stat("📸", photos, "Photos scanned")
        + _stat("📬", emails, "Care plans emailed")
        + "</div>"
    )


def landing_hero(features: Sequence[Tuple[str, str, str]]) -> str:
    cards = "".join(
        f'<div class="la-feature"><div class="la-feature-icon">{escape(icon)}</div>'
        f"<div><b>{escape(title)}</b><div>{escape(desc)}</div></div></div>"
        for icon, title, desc in features
    )
    return (
        '<div class="la-landing">'
        '<div class="la-eyebrow">AI PLANT CLINIC</div>'
        '<h1 class="la-title">Your plants, <em>diagnosed</em> in seconds.</h1>'
        "<p>Snap a photo of a struggling plant and get a clear diagnosis and care plan, "
        "straight to your inbox.</p>"
        f'<div class="la-features">{cards}</div></div>'
    )
