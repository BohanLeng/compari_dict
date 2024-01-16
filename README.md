# compari_dict

developed by Bohan Leng



## Usage: 
Typing and saving file with '@something', the script will translate 'something' into desired language(s) and write back into file in markdown table format. 

Currently supported editor: Pycharm built-in markdown editor


## To include your API keys
Create a configuration file `api_keys.ini`:
```ini
[API_KEYS]
GOOGLE_TRANS_API = YOUR_GOOGLE_API
DEEPL_API = YOUR_DEEPL_API
OPENAI_API = YOUR_OPENAI_API
```
Only write the API keys of the engines you intend to use. 
