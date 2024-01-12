import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import difflib
import os

head = "@@"


class NotebookProcessor(LoggingEventHandler):
    def __init__(self, file_path, logger=None):
        super().__init__()
        self.monitored_file = file_path
        with open(file_path, 'r') as file:
            self.previous_content = file.readlines()

    def on_modified(self, event):
        super().on_modified(event)
        if event.is_directory:
            # does not support dir for now
            raise ValueError("A directory was input, a file expected instead.")
        assert event.src_path == os.path.abspath(self.monitored_file)
        print(f'File {self.monitored_file} modification has been detected, processing...')
        self.diff_file()

    def diff_file(self):
        # Read the file and compare its content with the previous content
        with open(self.monitored_file, 'r') as file:
            new_content = file.readlines()
            diff = difflib.unified_diff(
                self.previous_content,
                new_content,
                lineterm='',  # output using newline character of input content
                fromfile='previous_content',
                tofile='new_content',
                n=1  # context line numbers shown in output
            )
            added_lines = [line[1:] for line in list(diff)[2:] if line.startswith('+')]
            if added_lines:
                print(f"{len(added_lines)} lines added:")
                for line in added_lines:
                    if line.startswith(head):
                        print(line)  # TODO
                # Do something with the changed content
            self.previous_content = new_content


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if len(sys.argv) < 2:
        raise ValueError("A file is required to monitor")
    path = sys.argv[1]
    event_handler = NotebookProcessor(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()