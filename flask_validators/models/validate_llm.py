from langid.langid import LanguageIdentifier, model as langid_model

def validate_language(value, desired_language):
    identifier = LanguageIdentifier.from_modelstring(langid_model, norm_probs=True)
    predicted_lang, _ = identifier.classify(value)

    if predicted_lang == desired_language:
        return True, None  # Value matches the desired language, return True and None

    return False, f'Value is not in the desired language ({desired_language}).'