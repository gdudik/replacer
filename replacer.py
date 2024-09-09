import os
import re
import time
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the path to the file to watch
FILE_PATH = os.path.abspath("./testfile.txt")

# Define your find-and-replace rules (as key-value pairs)
def load_csv():
    result_dict = {}
    with open('./definitions.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['find'].strip()
            value = row['replace'].strip()
            result_dict[key] = value
    return result_dict



def apply_find_replace(text, rules):
    """Applies find-and-replace rules to the text."""
    for find, replace in rules.items():
        text = re.sub(find, replace, text)  # You can use `re.sub` for regex patterns or `str.replace` for simple replacements
    return text

class FileChangeHandler(FileSystemEventHandler):
    """Custom event handler to react to file changes."""
    def on_modified(self, event):
        # Print the event source path for debugging
        # print(f"Detected change in: {event.src_path}")

        # Convert paths to absolute for comparison
        if os.path.abspath(event.src_path) == FILE_PATH:
            print(f"File {FILE_PATH} modified, applying find-and-replace...")
            self.process_file()

    def process_file(self):
        """Reads, processes, and writes back the modified file if there are changes."""
        try:
            # Read the current content of the file
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Apply find-and-replace rules
            modified_content = apply_find_replace(original_content, load_csv())

            # Only write back if the modified content is different from the original
            if modified_content != original_content:
                print(f"Content modified, writing changes to {FILE_PATH}")
                with open(FILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                print(f"Find-and-replace applied successfully to {FILE_PATH}")
            else:
                print("No changes detected, skipping write operation.")
        except Exception as e:
            print(f"Error processing file: {e}")

def start_watching():
    """Starts watching the file for modifications."""
    event_handler = FileChangeHandler()
    observer = Observer()

    # Get the directory of the file to watch
    file_dir = os.path.dirname(FILE_PATH)

    observer.schedule(event_handler, path=file_dir, recursive=False)
    observer.start()
    
    print(f"Started watching {FILE_PATH} for changes...")

    try:
        while True:
            time.sleep(1)  # Keep the script running to watch for file changes
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped watching.")
    
    observer.join()

if __name__ == "__main__":
    start_watching()
