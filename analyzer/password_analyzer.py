"""Local-only password analysis heuristics for educational use."""

import math
import re
import string

from .common_passwords import COMMON_PASSWORDS, KEYBOARD_PATTERNS, normalized_password


def _has_sequence(password: str) -> bool:
    lowered = password.lower()
    for index in range(len(lowered) - 2):
        chunk = lowered[index : index + 3]
        if chunk.isalpha() or chunk.isdigit():
            values = [ord(char) for char in chunk]
            if values[1] - values[0] == values[2] - values[1] and abs(values[1] - values[0]) == 1:
                return True
    return bool(re.search(r"(0123|1234|2345|3456|4567|5678|6789|abcd|bcde|cdef)", lowered))


def _has_excessive_repetition(password: str) -> bool:
    return bool(re.search(r"(.)\1{2,}", password))


def _has_date(password: str) -> bool:
    return bool(re.search(r"(19|20)\d{2}", password))


def _character_pool_size(password: str) -> int:
    pool = 0
    if any(char.islower() for char in password):
        pool += 26
    if any(char.isupper() for char in password):
        pool += 26
    if any(char.isdigit() for char in password):
        pool += 10
    if any(char in string.punctuation for char in password):
        pool += len(string.punctuation)
    return pool


def estimate_entropy(password: str) -> float:
    """Return a search-space estimate, not a prediction of cracking time."""
    if not password:
        return 0.0
    pool = _character_pool_size(password)
    return round(len(password) * math.log2(pool), 1) if pool else 0.0


def analyze_password(password: str) -> dict:
    length_ok = len(password) >= 12
    uppercase = any(char.isupper() for char in password)
    lowercase = any(char.islower() for char in password)
    numbers = any(char.isdigit() for char in password)
    symbols = any(not char.isalnum() for char in password)
    common = password.lower() in COMMON_PASSWORDS or normalized_password(password) in COMMON_PASSWORDS
    sequence = _has_sequence(password)
    repeated = _has_excessive_repetition(password)
    date = _has_date(password)
    keyboard = any(pattern in password.lower() for pattern in KEYBOARD_PATTERNS)

    checks = {
        "length": length_ok,
        "uppercase": uppercase,
        "lowercase": lowercase,
        "numbers": numbers,
        "symbols": symbols,
        "not_common": not common,
        "no_sequences": not sequence,
        "no_excessive_repetition": not repeated,
    }
    warnings = []
    if not password:
        warnings.append("Enter a password to begin analysis.")
    if len(password) < 12:
        warnings.append("Use at least 12 characters.")
    if common:
        warnings.append("This matches a common password or predictable substitution.")
    if not uppercase:
        warnings.append("Add uppercase letters.")
    if not lowercase:
        warnings.append("Add lowercase letters.")
    if not numbers:
        warnings.append("Add numbers only when they are not predictable.")
    if not symbols:
        warnings.append("Add special characters.")
    if sequence:
        warnings.append("Avoid simple sequences such as 1234 or abcd.")
    if repeated:
        warnings.append("Avoid excessive repeated characters.")
    if date:
        warnings.append("Avoid dates and other personal information.")
    if keyboard:
        warnings.append("Avoid keyboard patterns such as qwerty.")

    score = min(100, len(password) * 3)
    score += sum(8 for flag in (uppercase, lowercase, numbers, symbols) if flag)
    score += min(12, max(0, len(set(password)) - 4) * 2)
    if len(password) >= 16:
        score += 8
    if common:
        score -= 45
    if sequence:
        score -= 15
    if repeated:
        score -= 15
    if date:
        score -= 10
    if keyboard:
        score -= 15
    score = max(0, min(100, score))

    if score < 25:
        strength = "Very Weak"
    elif score < 45:
        strength = "Weak"
    elif score < 70:
        strength = "Moderate"
    elif score < 88:
        strength = "Strong"
    else:
        strength = "Very Strong"

    recommendations = warnings[:]
    if not recommendations:
        recommendations = [
            "Your password has good length and character diversity.",
            "Avoid reusing it on multiple websites.",
            "Consider storing unique passwords in a password manager.",
        ]
    return {
        "score": score,
        "strength": strength,
        "entropy": estimate_entropy(password),
        "checks": checks,
        "warnings": warnings,
        "recommendations": recommendations,
    }
