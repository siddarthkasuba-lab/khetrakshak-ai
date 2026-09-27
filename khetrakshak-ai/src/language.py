"""
language.py

Regional-language text output, plus the on-device TTS hook.

Only a small demo phrase table is included here (English + Hindi) -- in the
full build this expands to the other major regional languages and a proper
translation layer, but the interface (translate() / speak()) stays the same.
"""

from typing import Dict

_PHRASES: Dict[str, Dict[str, str]] = {
    "diagnosis_header": {
        "en": "Diagnosis",
        "hi": "\u0928\u093f\u0926\u093e\u0928",  # निदान
    },
    "treatment_header": {
        "en": "Recommended Treatment",
        "hi": "\u0905\u0928\u0941\u0936\u0902\u0938\u093f\u0924 \u0909\u092a\u091a\u093e\u0930",  # अनुशंसित उपचार
    },
    "schemes_header": {
        "en": "Schemes You May Be Eligible For",
        "hi": "\u092f\u094b\u091c\u0928\u093e\u090f\u0901 \u091c\u093f\u0928\u0915\u0947 \u0932\u093f\u090f \u0906\u092a \u092a\u093e\u0924\u094d\u0930 \u0939\u094b \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",  # योजनाएँ जिनके लिए आप पात्र हो सकते हैं
    },
    "no_disease": {
        "en": "No disease detected. Keep monitoring your crop.",
        "hi": "\u0915\u094b\u0908 \u0930\u094b\u0917 \u0928\u0939\u0940\u0902 \u092a\u093e\u092f\u093e \u0917\u092f\u093e\u0964 \u0905\u092a\u0928\u0940 \u092b\u0938\u0932 \u0915\u0940 \u0928\u093f\u0917\u0930\u093e\u0928\u0940 \u091c\u093e\u0930\u0940 \u0930\u0916\u0947\u0902\u0964",
    },
}


def translate(key: str, language: str = "en") -> str:
    entry = _PHRASES.get(key, {})
    return entry.get(language, entry.get("en", key))


def speak(text: str, language: str = "en") -> None:
    """
    On-device TTS hook.

    In the Windows build this calls the platform's on-device speech
    synthesis (e.g. Windows SAPI voices for the target regional language)
    so no cloud TTS API is ever called. This prototype just prints what
    would be spoken, so the pipeline is runnable without an audio device.
    """
    print(f"[TTS - {language}] {text}")
