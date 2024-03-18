# compari_dict

Learning languages can be fun when comparing with other languages. Observe the similarities and differences between same expressions in different languages help you understand and memorise them better.

This tool provides you a shortcut instead of looking up multiple dictionaries, or hitting translate button multiple times and pasting to your notes. You don't need to go through any difficulties before you can feel the beautiful nuances of languages. 

## Supported tranlation Engines:
- [x] [Google Cloud Translation](https://cloud.google.com/translate/)
- [x] [DeepL Translator](https://www.deepl.com/pro-api?cta=header-pro-api)
- [ ] [OpenAI](https://platform.openai.com)


## Usage
### Original text

>  NOTE: In source mode of Markdown editors, there should be no blank line between lines. 

Comment te dire adieu ?

@Goodbye

Was ist das?

@This is a translator to multiple languages

Something to drink?

@@

orange juice

apple juice

Coca-Cola

water

coffee

tea

cappuccino

red wine

white wine

milk

beer

iced tea


### Execute:
`$python3 converter.py README.md en de fr zh -e "Google Trans"`

### Output:
Comment te dire adieu ?

|Goodbye|Auf Wiedersehen|Au revoir|再见|
|-|-|-|-|

Was ist das ?

|This is a translator to multiple languages|Dies ist ein Übersetzer für mehrere Sprachen|Ceci est un traducteur vers plusieurs langues|这是多语言翻译器|
|-|-|-|-|

Something to drink?

|en|de|fr|zh|
|-|-|-|-|
|orange juice|Orangensaft|jus d&#39;orange|橙汁|
|apple juice|Apfelsaft|jus de pomme|苹果汁|
|Coca-Cola|Coca-Cola|Coca-Cola|可口可乐|
|water|Wasser|eau|水|
|coffee|Kaffee|café|咖啡|
|tea|Tee|thé|茶|
|cappuccino|Cappuccino|cappuccino|卡布奇诺|
|red wine|Rotwein|vin rouge|红酒|
|white wine|Weißwein|vin blanc|白酒|
|milk|Milch|lait|牛奶|
|beer|Bier|bière|啤酒|
|iced tea|Eistee|thé glacé|冰茶|


## Common text editors' support

This feature converts text file in the background, so this requires editors that supports loading file from disk automatically.

Some editors are tested.

- **Obsidian &check;** 
- Sublime Text &check; 
- Typora &cross;
- Pycharm built-in markdown editor &check; 

Obsidian's community plugins allow us to execute command inside terminals embedded in Obsidian editor window. Moreover, this project is planned to be an Obsidian plugin.  

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


