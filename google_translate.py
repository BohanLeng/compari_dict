from base_translator import BaseTranslator
import requests


class GoogleTranslator(BaseTranslator):
    def __init__(self, auth_key):
        super().__init__(auth_key)
        self.url = 'https://translation.googleapis.com/language/translate/v2'
        self.auth_key = auth_key

    def translate_request(self, text, source_language, target_language):
        params = {
            'key': self.auth_key,
            'q': text,
            'source': source_language,
            'target': target_language
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            translation = response.json()['data']['translations'][0]['translatedText']
            print(f"{text} -> {translation}\t({source_language} -> {target_language})")
            return translation
        else:
            print("Translation Failed:", response.json())
