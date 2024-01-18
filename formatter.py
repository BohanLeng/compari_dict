def format_line_results(word, results):
    md_table = f"\n|{word}|"
    for result in results:
        assert result, "No result to format" # TODO single @ will cause assertion fail
        md_table = md_table + result + '|'
    md_table = md_table + '\n|-|' + len(results) * '-|' + '\n\n'
    return md_table


def format_table_results(source_words, translated_matrix):
    md_table = '\n'
    for i in range(len(source_words)):
        md_row = f"|{source_words[i]}|"
        for col in translated_matrix:
            md_row = md_row + col[i] + '|'
        md_table = md_table + md_row + '\n'
        if i == 0:
            md_table = md_table + ('|-|' + len(translated_matrix) * '-|' + '\n')
    print(md_table)
    return md_table + '\n'
