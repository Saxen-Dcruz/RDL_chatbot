# test_guardrails.py
from guardrails_setup import create_simple_guard, create_content_guard
from guardrails.errors import ValidationError


def test_profanity_guard():
    """Test the profanity guardrail."""
    guard = create_simple_guard()
    
    # Test clean text
    clean_text = "Hello, how are you today?"
    result = guard.validate(clean_text)
    print("---- Profanity Guard: Clean Text ----")
    print(f"Input: {clean_text}")
    print(f"Output: {result.validated_output}")
    print(f"Success: {result.validation_passed}")
    print()
    
    # Test text with profanity
    profane_text = "This is a fucking test with shit words"
    result = guard.validate(profane_text)
    print("---- Profanity Guard: Profane Text ----")
    print(f"Input: {profane_text}")
    print(f"Output: {result.validated_output}")
    print(f"Success: {result.validation_passed}")
    if hasattr(result, 'error_message'):
        print(f"Error: {result.error_message}")
    print()


def test_length_guard():
    """Test the safe string length guardrail."""
    guard = create_content_guard()  # contains both profanity + length

    # Test valid length
    short_text = "This is within the allowed length."
    result = guard.validate(short_text)
    print("---- Length Guard: Short Text ----")
    print(f"Input: {short_text}")
    print(f"Output: {result.validated_output}")
    print(f"Success: {result.validation_passed}")
    print()

    # Test overly long text
    long_text = "x" * 2500 # 600 chars, exceeds default max_len=500
    try:
        result = guard.validate(long_text)
        print("---- Length Guard: Long Text ----")
        print(f"Input length: {len(long_text)}")
        print(f"Output: {result.validated_output}")
        print(f"Success: {result.validation_passed}")
        if hasattr(result, 'error_message'):
            print(f"Error: {result.error_message}")
    except ValidationError as e:
        print("---- Length Guard: Long Text ----")
        print(f"Input length: {len(long_text)}")
        print(f"❌ ValidationError: {e}")
    print()


if __name__ == "__main__":
    test_profanity_guard()
    test_length_guard()
