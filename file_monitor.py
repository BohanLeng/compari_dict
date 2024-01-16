import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import difflib
import os
import fcntl
from multi_translator import MultiTranslator


head = '@'
engine = 'DeepL'
# 'Google Trans' / 'DeepL' / 'OpenAI'
source_language = 'de'
target_languages = ['en-gb', 'fr']


class NotebookProcessor(LoggingEventHandler):
    def __init__(self, file_path, translator):
        super().__init__()
        self.translator = translator
        self._monitored_file = file_path
        with open(file_path, 'r') as file:
            self._previous_content = file.readlines()
            self._new_content = self._previous_content
        self.ignore_next_change = False

    def on_modified(self, event):   # TODO saving by file swapping not being detected
        if self.ignore_next_change:
            self.ignore_next_change = False
            return
        super().on_modified(event)
        if event.is_directory:
            # does not support dir for now
            raise ValueError("A directory was input, a file expected instead.")
        assert event.src_path == os.path.abspath(self._monitored_file)
        print(f'File {self._monitored_file} modification has been detected, processing...')
        self.diff_file()

    def diff_file(self):
        # Read the file and compare its content with the previous content
        with open(self._monitored_file, 'r') as file:
            self._new_content = file.readlines()
        diff = difflib.unified_diff(
            self._previous_content,
            self._new_content,
            lineterm='',  # output using newline character of input content
            fromfile='previous_content',
            tofile='new_content',
            n=1  # context line numbers shown in output
        )
        added_lines = [line[1:] for line in list(diff)[2:] if line.startswith('+' + head)]
        if added_lines:
            for i, line in enumerate(self._new_content):
                if line in added_lines:
                    word = line.strip()[1:]
                    results = self.translator.translate(word)
                    if results:
                        self._new_content[i] = format_results(word, results)
                    else:
                        print("No translation results.")
            self.ignore_next_change = True
            with open(self._monitored_file, 'w') as file:
                fcntl.flock(file, fcntl.LOCK_EX)
                file.writelines(self._new_content)
                fcntl.flock(file, fcntl.LOCK_UN)
        else:
            print("Detected No line to be translated, waiting for next change...")
        self._previous_content = self._new_content


def format_results(word, results):
    md_table = f"\n|{word}|"
    for result in results:
        assert result, "No result to format"
        md_table = md_table + result + '|'
    md_table = md_table + '\n|-|' + len(results) * '-|' + '\n\n'
    return md_table


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if len(sys.argv) < 2:
        raise ValueError("A file is required to monitor")
    mt_translator = MultiTranslator(engine, source_language, target_languages)
    path = sys.argv[1]
    event_handler = NotebookProcessor(path, mt_translator)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()