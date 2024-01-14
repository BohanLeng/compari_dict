import requests


def translate_text(api_key, text, source_language, target_language):
    print(api_key)
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = {
        'key': api_key,
        'q': text,
        'source': source_language,
        'target': target_language
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        translation = response.json()['data']['translations'][0]['translatedText']
        print(f"{text} -> {translation}\t({source_language} -> {target_language})")
        return translation
    else:
        print("Translation Failed:", response.json())
