import os
import re
import time
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from termcolor import colored

os.system('color')

# Define the path to the file to watch
print(colored("Welcome to the replacer. Before proceeding, create a 'definitions.csv' \nfile and place it in the same folder as this program. \nA definitions file should be a csv where each \nrow contains a record of a string you'd like to replace, and the string you'd like to replace it with. There should be no header.\nExample:",'blue'))
print(colored("`Varsity Boys 100 Meter Dash, Boys 100\nJV Girls 200 Meter Dash, JV Girls 200`", 'yellow'))
print(colored("This program will automatically watch the evt file you specify and apply the changes whenever the file is updated.", 'blue'))
entered_path = input('Enter path to evt file: ')
entered_path = entered_path.strip('\'"')
FILE_PATH = os.path.abspath(entered_path)

# Define your find-and-replace rules (as key-value pairs)
def load_csv():
    result_dict = {}
    with open('./definitions.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                result_dict[key] = value
            else:
                print(f'Skipping row {row} due to insufficient data')
    return result_dict



def apply_find_replace(text, rules):
    """Applies find-and-replace rules to the text."""
    for find, replace in rules.items():
        text = re.sub(find, replace, text)  # You can use `re.sub` for regex patterns or `str.replace` for simple replacements
    return text

class FileChangeHandler(FileSystemEventHandler):
    """Custom event handler to react to file changes."""
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == FILE_PATH:
            print(f"File {FILE_PATH} modified, applying find-and-replace...")
            self.process_file()
    
    def on_created(self, event):
        if os.path.abspath(event.src_path) == FILE_PATH:
            print(f"File {FILE_PATH} created, applying find-and-replace...")
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
