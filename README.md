# File Renamer

File Renamer is a Python application with a graphical user interface that allows users to rename multiple files based on their content. It specifically looks for a "Title:" field within the first 5 lines of text and markdown files to determine the new filename.

## Features

- Select multiple files and directories for processing
- Rename files based on their content
- Handle duplicate filenames
- Progress bar to show renaming progress
- Support for text (.txt) and markdown (.md) files

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system
- PyQt6 library installed

## Installation

1. Clone this repository or download the `tre.py` file.

2. Install the required dependency:
```
pip install PyQt6
```

## Usage

To run the File Renamer application:

1. Open a terminal or command prompt.
2. Navigate to the directory containing `tre.py`.
3. Run the following command:
```
python tre.py
```

4. The File Renamer GUI will appear.
5. Click "Add Files/Directories" to select files or folders for processing.
6. Use "Remove Selected" to remove any unwanted items from the list.
7. Click "Rename Files" to start the renaming process.
8. A progress bar will show the renaming progress.
9. Once complete, a message will confirm the process has finished.

## How it works

1. The application scans the selected files and directories.
2. For each .txt or .md file, it reads the first 5 lines.
3. It looks for a line starting with "Title:".
4. If found, it uses the text after "Title:" as the new filename.
5. The new filename is sanitized to remove invalid characters.
6. If a file with the new name already exists, a number is appended to avoid overwriting.
7. The file is then renamed with its new name, keeping the original extension.

## Note

Always make sure you have backups of your files before running any batch renaming operations.
