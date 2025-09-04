from guardrails import Guard
from guardrails_validators import ProfanityFree, SafeStringLength  

def create_simple_guard(max_chars: int = 2000):
    """Create a guard with profanity filter (auto-fixes text) + length check."""
    guard = (
        Guard()
        .use(SafeStringLength(max_len=max_chars, on_fail="exception"))  # ⬅️ length limit
        .use(ProfanityFree(on_fail="fix"))  # ⚡ replaces bad words, still passes
    )
    return guard

def create_content_guard(max_chars: int = 2000):
    """Create a stricter guard that blocks profanity entirely + length check."""
    guard = (
        Guard()
        .use(SafeStringLength(max_len=max_chars, on_fail="exception"))  # ⬅️ length limit
        .use(ProfanityFree(on_fail="exception"))  # ❌ fails validation if profanity
    )
    return guard