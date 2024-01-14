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
            import google_translate
            self.translate_call = google_translate.translate_text
            self.api_key = config.get('API_KEYS', 'GOOGLE_TRANS_API')
        elif self.engine == 'DeepL':
            # self.api_key = config.get('API_KEYS', 'DEEPL_API')    # TODO
            pass
        elif self.engine == 'OpenAI':
            # self.api_key = config.get('API_KEYS', 'DEEPL_API')    # TODO
            pass

    def translate(self, word):
        results = []
        for lang in self.target_langues:
            results.append(self.translate_call(self.api_key, word, self.src_lang, lang))
        return results
