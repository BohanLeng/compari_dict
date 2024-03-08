import os
import sys
import argparse
from multi_translator import MultiTranslator
import formatter

head = '@'
default_engine = 'Google Trans'
segment_symbol = '+'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converting texts into multi-linguistic tables.')
    parser.add_argument('file_to_process', type=str, help='Path to the file to process')
    # source_language = 'de'
    parser.add_argument('source_language', type=str, help='Code of source language')
    # target_languages = ['en-gb', 'fr']
    parser.add_argument('target_languages', type=str, nargs='+', help='Codes of target language code')
    # 'Google Trans' / 'DeepL' / 'OpenAI'
    parser.add_argument('--translation_engine', '-e', type=str, help='Google Trans / DeepL')
    # eg. api_keys.ini
    parser.add_argument('--api_config_file', '-c', type=str, help="Config file containing api keys")
    args = parser.parse_args()
    source_language = args.source_language
    target_languages = args.target_languages
    if args.translation_engine and args.translation_engine in ['Google Trans', 'DeepL', 'OpenAI']:
        engine = args.translation_engine
    else:
        exit('Unsupported engine')
    if args.api_config_file and os.path.exists(args.api_config_file):
        mt_translator = MultiTranslator(engine, source_language, target_languages, args.api_config_file)
    else:
        mt_translator = MultiTranslator(engine, source_language, target_languages)
    file_path = args.file_to_process
    with open(file_path, 'r') as file:
        content = file.readlines()
        # Detect multiple lines starting with a 'head * 2' line
        sections = []
        section = []
        in_section = False
        last_line_index = len(content) - 1
        # Detect lines between a line with head * 2 and a blank line
        for i, line in enumerate(content):
            if line.startswith(head * 2):
                in_section = True
            if in_section:
                if line.strip():
                    section.append(line)
                if not line.strip() or i == last_line_index:
                    in_section = False
                    sections.append(section)
                    section = []
        translated_sections = []
        for section in sections:
            words = [line.strip() for line in section[1:]]
            words_combined = segment_symbol.join(words)
            results_combined = mt_translator.translate(words_combined)
            if results_combined:
                results_matrix = [col.split(segment_symbol) for col in results_combined]
                for col in results_matrix:
                    assert len(words) == len(col), "Some words are missing while translation. Exiting..."
                formatted_section = formatter.format_table_results(words, results_matrix, source_language, target_languages)
                translated_sections.append(formatted_section)
    with open(file_path, 'r') as file:
        content = file.readlines()
        # Process multiple lines
        in_section = False
        lines_count = len(content)  # Keep track for added lines
        for i, line in enumerate(content):
            if line.startswith(head * 2):
                in_section = True
                start_index = i
                content[i] = ''
                i = i + 1
                continue
            if in_section:
                if line.strip():
                    content[i] = ''
                    if i != lines_count - 1:
                        continue
                in_section = False
                content[i] = translated_sections.pop(0)
                if not translated_sections:
                    break

        # Section words now transformed into table.
        # even if head exists in sections (not expected),
        # now already dealt with.
        # Starting processing single words
        words = [line.strip()[1:] for line in content if line.startswith(head)]
        words_combined = segment_symbol.join(words)
        results_combined = mt_translator.translate(words_combined)
        if results_combined:
            translated_lines = []
            results_matrix = [col.split(segment_symbol) for col in results_combined]
            # for col in results_matrix:
            #     assert len(words) == len(col), "Some words are missing while translation. Exiting..."
            for i, word in enumerate(words):
                results_row = [col[i] for col in results_matrix]
                translated_lines.append(formatter.format_line_results(word, results_row))
        for i, line in enumerate(content):
            if line.startswith(head):
                content[i] = translated_lines.pop(0)
    print("Results received and formatted, writing back to file...")
    with open(file_path, 'w') as file:
        file.writelines(content)
    print("Writing complete!")
