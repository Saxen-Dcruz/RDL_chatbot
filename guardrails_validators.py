from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

# ----------------- PROFANITY VALIDATOR -----------------
@register_validator(name="profanity_free", data_type="string")
class ProfanityFree(Validator):
    """Validator to check if content contains inappropriate language."""

    def __init__(self, on_fail: str = None, **kwargs):
        super().__init__(on_fail=on_fail, **kwargs)
        self.inappropriate_words = {
            # Common profanity
            "fuck", "fucking", "fucked", "motherfucker", "mf", "fucker",
            "shit", "bullshit", "horseshit", "shithead", "dumbshit",
            "bitch", "sonofabitch", "slut", "whore", "hoe", "thot",
            "ass", "asshole", "dumbass", "jackass", "smartass", "fatass",
            "bastard", "prick", "dick", "cock", "dildo", "pussy", "cunt", 
            "twat", "clit", "ballsack", "nutsack", "scrotum",

            # Sexual insults
            "cum", "jizz", "spooge", "jizzbag", "jerkoff", "wanker", 
            "piss", "pissing", "pissed", "pisshead",
            "boner", "fapping", "douche", "douchebag", "buttplug",

            # Homophobic & derogatory slurs
            "faggot", "fag", "dyke", "tranny", "homo", "queer",
            "lesbo", "butch",

            # Racist/ethnic slurs
            "nigger", "nigga", "chink", "gook", "spic", "wetback", 
            "beaner", "cracker", "redneck", "savage", "paki", "towelhead", 
            "sandnigger", "coon", "jigaboo", "porchmonkey", "ape",

            # Ableist & other offensive terms
            "retard", "retarded", "spaz", "cripple", "lame", "idiot",
            "moron", "imbecile", "dumbfuck",

            # Misc extreme insults
            "kill yourself", "kms", "die", "hang yourself", "suicide bait",
            "worthless", "useless", "piece of shit", "garbage",
        }

    def validate(self, value: any, metadata: dict) -> ValidationResult:
        if not isinstance(value, str):
            return FailResult(error_message="Value must be a string")

        value_lower = value.lower()
        found_profanity = [w for w in self.inappropriate_words if w in value_lower]

        if found_profanity:
            return FailResult(
                error_message="Profanity detected",
                fix_value="Your query contains inappropriate language. Please rephrase."
            )

        return PassResult(output=value)


# ----------------- STRING LENGTH VALIDATOR -----------------
@register_validator(name="safe_string_length", data_type="string")
class SafeStringLength(Validator):
    """Validator to ensure the string is within allowed length limits."""

    def __init__(self, max_len: int = 2000, on_fail: str = None, **kwargs):
        super().__init__(on_fail=on_fail, **kwargs)
        self.max_len = max_len

    def validate(self, value: any, metadata: dict) -> ValidationResult:
        if not isinstance(value, str):
            return FailResult(error_message="Value must be a string")

        if len(value) > self.max_len:
            return FailResult(
                error_message=f"Your query is too long (limit {self.max_len} characters). Please rephrase and try again.",
                fix_value="Your query is too long. Please rephrase within the allowed limit."
            )

        return PassResult(output=value)
