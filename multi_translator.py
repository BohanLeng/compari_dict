import os
from configparser import ConfigParser


class MultiTranslator:
    def __init__(self, engine, src_lang, target_langues):
        self.src_lang = src_lang
        self.target_langues = target_langues
        self.engine = engine
        config = ConfigParser()
        config.read('api_keys.ini')
        if self.engine == 'Google Trans':
            api_key = config.get('API_KEYS', 'GOOGLE_TRANS_API')
            from google_translate import GoogleTranslator
            self.the_translator = GoogleTranslator(api_key)
        elif self.engine == 'DeepL':
            api_key = config.get('API_KEYS', 'DEEPL_API')
            from deepl_translate import DeepLTranslator
            self.the_translator = DeepLTranslator(api_key)
        elif self.engine == 'OpenAI':
            api_key = config.get('API_KEYS', 'DEEPL_API')    # TODO
            pass
        self.translate_call = self.the_translator.translate_request

    def translate(self, text):
        results = []
        for lang in self.target_langues:
            results.append(self.translate_call(text, self.src_lang, lang))
        return results
