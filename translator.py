from deep_translator import GoogleTranslator

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru",
    "Korean": "ko"
}


def translate_text(text, source, target):
    translator = GoogleTranslator(
        source=LANGUAGES[source],
        target=LANGUAGES[target]
    )
    return translator.translate(text)