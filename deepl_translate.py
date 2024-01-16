from base_translator import BaseTranslator
import requests


class DeepLTranslator(BaseTranslator):
    def __init__(self, auth_key):
        super().__init__(auth_key)
        self.url = "https://api-free.deepl.com/v2/translate"  # To use paid version, remove '-free' in url
        self.headers = {
            "Authorization": f"DeepL-Auth-Key {auth_key}",
            "Content-Type": "application/json",
        }

    def translate_request(self, text, source_language, target_language):
        request_data = {
            "text": [text],
            "source_lang": source_language,
            "target_lang": target_language
        }
        response = requests.post(self.url, json=request_data, headers=self.headers)
        if response.status_code == 200:
            translation = response.json()['translations'][0]['text']
            print(f"{text} -> {translation}\t({source_language} -> {target_language})")
            return translation
        else:
            print("Translation Failed:", response.json())

