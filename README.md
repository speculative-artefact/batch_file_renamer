# Batch File Renamer

A simple desktop application built with Python and PyQt6 for batch renaming or copying files within a specified directory.

## Features

*   Browse to a target directory.
*   Navigate up the directory structure.
*   Choose between renaming files in place or copying them with new names.
*   Optionally include subdirectories (recursive search).
*   Filter files by specific extensions (TXT, MA, PNG supported by default).
*   Filter files shown in the browser by supported types.
*   Add a prefix and/or suffix to filenames.
*   Find and replace specific strings within filenames.
*   Quickly swap find and replace strings.
*   Displays the total number of files found based on filters.
*   Provides status updates during the renaming/copying process.

## How to Run

1.  Ensure you have Python and PyQt6 installed (`pip install PyQt6`).
2.  Run the application using: `python batch_renamer_gui_starter.py`
3.  Use the "Browse" button to select the directory containing the files you want to modify.
4.  Configure the options (Method, Include subfolders, Filetypes, Prefix/Suffix, Find/Replace).
5.  Click the "Rename" (or "Copy" depending on the method selected) button to start the process.

## Project Structure

*   `batch_renamer_gui_starter.py`: Main application script, handles the GUI logic and user interactions.
*   `batch_renamer_lib.py`: Core library containing the logic for finding and renaming/copying files.
*   `batch_renamer.ui`: Qt Designer file defining the user interface layout.
*   `batch_renamer_ui.py`: Python code generated from `batch_renamer.ui` using `pyuic6`.
*   `MakeUIPy.bat`: Batch script to regenerate `batch_renamer_ui.py` from `batch_renamer.ui`.
*   `README.md`: This file.
*   `TODO.md`: List of potential improvements and tasks.
