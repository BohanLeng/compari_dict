def format_line_results(word, results):
    md_table = f"\n|{word}|"
    for result in results:
        assert result, "No result to format" # TODO single @ will cause assertion fail
        md_table = md_table + result + '|'
    md_table = md_table + '\n|-|' + len(results) * '-|' + '\n'
    return md_table


def format_table_results(source_words, translated_matrix, source_langue, target_langues):
    md_table = f'\n|{source_langue}|' + ''.join([target_langue + '|' for target_langue in target_langues])
    md_table += '\n' + '|-|' + len(target_langues) * '-|' + '\n'
    for i in range(len(source_words)):
        md_row = f"|{source_words[i]}|" + ''.join([col[i] + '|' for col in translated_matrix])
        md_table += md_row + '\n'
    print(md_table)
    return md_table + '\n'
