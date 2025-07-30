# modules/translator.py
import argostranslate.package
import argostranslate.translate

def translate_to_english(text, source_lang_code):
    """
    Translates text from a source language to English using Argos Translate.
    """
    if source_lang_code == "en":
        return text # No translation needed

    print(f"-> [Translator] Translating from '{source_lang_code}' to 'en'...")
    try:
        # Find the installed translation package
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(lambda x: x.code == source_lang_code, installed_languages))[0]
        to_lang = list(filter(lambda x: x.code == "en", installed_languages))[0]
        
        translation = from_lang.get_translation(to_lang)
        return translation.translate(text)
    except IndexError:
        print(f"!! [Translator] Language pack for '{source_lang_code}' to 'en' not found. Please install it.")
        return text # Return original text if translation fails
    except Exception as e:
        print(f"!! [Translator] Error: {e}")
        return text
