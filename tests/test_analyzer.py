from analyzer.password_analyzer import analyze_password, estimate_entropy
from analyzer.password_generator import generate_password


def test_empty_password_is_very_weak():
    result = analyze_password("")
    assert result["strength"] == "Very Weak"
    assert result["score"] == 0


def test_common_password_is_detected():
    result = analyze_password("P@ssw0rd")
    assert result["checks"]["not_common"] is False
    assert any("common" in warning.lower() for warning in result["warnings"])


def test_sequence_and_repetition_are_detected():
    result = analyze_password("aaa1234")
    assert result["checks"]["no_sequences"] is False
    assert result["checks"]["no_excessive_repetition"] is False


def test_long_diverse_password_is_strong():
    result = analyze_password("Raven!Orbit7-Copper$Lime")
    assert result["score"] >= 70
    assert result["strength"] in {"Strong", "Very Strong"}


def test_entropy_increases_with_length():
    assert estimate_entropy("Ab1!") < estimate_entropy("Ab1!Ab1!Ab1!")


def test_generator_length_and_character_requirements():
    password = generate_password(20, {"uppercase": True, "lowercase": True, "numbers": True, "symbols": True})
    assert len(password) == 20
    assert any(char.isupper() for char in password)
    assert any(char.islower() for char in password)
    assert any(char.isdigit() for char in password)
    assert any(not char.isalnum() for char in password)


def test_generator_rejects_invalid_options():
    try:
        generate_password(8, {"uppercase": False, "lowercase": False, "numbers": False, "symbols": False})
    except ValueError as error:
        assert "at least one" in str(error)
    else:
        raise AssertionError("Expected ValueError")
