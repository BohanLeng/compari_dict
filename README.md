# compari_dict

developed by Bohan Leng



## Usage: 
Typing and saving file with '@something', the script will translate 'something' into desired language(s) and write back into file in Markdown table format. 

Known supported editors: 

- Pycharm built-in markdown editor
- Sublime Text
- **Obsidian (Recommended)**


## To include your API keys
- Create a configuration file `api_keys.ini`:
```ini
[API_KEYS]
GOOGLE_TRANS_API = YOUR_GOOGLE_API
DEEPL_API = YOUR_DEEPL_API
OPENAI_API = YOUR_OPENAI_API
```
- Alternatively, you can specify your api keys in the environment settings:
Use the command `vim ~/.zshrc` (or the shell you are using), append
```shell
export GOOGLE_TRANS_API='YOUR_GOOGLE_API'
export DEEPL_API='YOUR_DEEPL_API'
export OPENAI_API_KEY='YOUR_OPENAI_API'
```
Then refresh your shell settings with `source ~/.zshrc` (or the shell you are using).

**For both methods, you only need to include the API keys of the engines you intend to use.**


