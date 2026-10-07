"""Cryptographically secure password generation."""

import secrets
import string

CHARACTER_SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{}:,.?",
}


def generate_password(length: int = 16, options: dict[str, bool] | None = None) -> str:
    """Generate a password with at least one character from every enabled set."""
    if not 8 <= length <= 32:
        raise ValueError("Length must be between 8 and 32.")

    selected = options or {name: True for name in CHARACTER_SETS}
    enabled = [name for name in CHARACTER_SETS if selected.get(name, False)]
    if not enabled:
        raise ValueError("Select at least one character type.")
    if length < len(enabled):
        raise ValueError("Length is too short for the selected character types.")

    required = [secrets.choice(CHARACTER_SETS[name]) for name in enabled]
    alphabet = "".join(CHARACTER_SETS[name] for name in enabled)
    result = required + [secrets.choice(alphabet) for _ in range(length - len(required))]
    secrets.SystemRandom().shuffle(result)
    return "".join(result)
