import sys
from multi_translator import MultiTranslator
import formatter

head = '@'
engine = 'DeepL'
# 'Google Trans' / 'DeepL' / 'OpenAI'
source_language = 'de'
target_languages = ['en-gb', 'fr']


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("The file to convert to be specified! Exiting...")
    mt_translator = MultiTranslator(engine, source_language, target_languages)
    file_path = sys.argv[1]
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
            words_combined = '+'.join(words)
            results_combined = mt_translator.translate(words_combined)
            if results_combined:
                results_matrix = [col.split('+') for col in results_combined]
                formatted_section = formatter.format_table_results(words, results_matrix)
                translated_sections.append(formatted_section)
    with open(file_path, 'r') as file:
        content = file.readlines()
        # Process multiple lines
        in_section = False
        lines_count = len(content)  # Keep track for added lines
        i = 0
        while i < lines_count:
            if content[i].startswith(head * 2):
                in_section = True
                start_index = i
                content[i] = ''
                i = i + 1
                continue
            if in_section:
                if content[i].strip():
                    content[i] = ''
                    if i == lines_count - 1:
                        in_section = False
                        content.insert(start_index, translated_sections.pop(0))
                        lines_count = lines_count + 1
                else:
                    in_section = False
                    content.insert(start_index, translated_sections.pop(0))
                    lines_count = lines_count + 1
                if not translated_sections:
                    break
            i = i + 1
        # Section words now transformed into table.
        # even if head exists in sections (not expected),
        # now already dealt with.
        # Starting processing single words
        words = [line.strip()[1:] for line in content if line.startswith(head)]
        words_combined = '+'.join(words)
        results_combined = mt_translator.translate(words_combined)
        if results_combined:
            translated_lines = []
            results_matrix = [col.split('+') for col in results_combined]
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
