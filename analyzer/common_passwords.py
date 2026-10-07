"""Small, educational common-password corpus and pattern helpers."""

COMMON_PASSWORDS = frozenset(
    {
        "123456",
        "12345678",
        "123456789",
        "1234567890",
        "123123",
        "111111",
        "000000",
        "password",
        "password123",
        "passw0rd",
        "qwerty",
        "qwerty123",
        "admin",
        "admin123",
        "letmein",
        "welcome",
        "abc123",
        "iloveyou",
        "monkey",
        "dragon",
        "login",
        "welcome123",
    }
)

KEYBOARD_PATTERNS = (
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "qazwsx",
    "1qaz",
    "2wsx",
)

SUBSTITUTION_NORMALIZATION = str.maketrans({"@": "a", "4": "a", "3": "e", "1": "i", "!": "i", "0": "o", "$": "s", "5": "s", "7": "t"})


def normalized_password(password: str) -> str:
    return password.lower().translate(SUBSTITUTION_NORMALIZATION)
