# TODO List - Batch File Renamer Improvements

This file lists potential improvements and tasks for the Batch File Renamer project.

## Code Refactoring & Robustness

*   **Decouple Library from GUI:**
    *   Remove `QMessageBox` usage from `batch_renamer_lib.py`. The library should return status codes/messages or raise exceptions, and the GUI (`batch_renamer_gui_starter.py`) should handle displaying them.
    *   Consider replacing GUI callback functions (`update_status`, `update_list`) passed to the library with a more standard approach like signals/slots if integrating deeper with Qt, or returning detailed results for the GUI to process.
*   **Improve Error Handling:**
    *   Add `try...except` blocks in `batch_renamer_lib.py` for file operations (e.g., `os.walk`, `os.listdir`, `shutil.move`, `shutil.copy`) to handle potential `FileNotFoundError`, `PermissionError`, etc. Report these errors back to the GUI.
    *   Handle potential errors in `get_renamed_file_path` (e.g., filenames without extensions when adding suffix).
    *   Validate user input (e.g., ensure find/replace strings are valid if using regex in the future).
*   **Fix `get_renamed_file_path` Bug:** When `string_to_find` is a list, the current implementation only replaces the *last* string in the list because `new_name` is overwritten in each iteration. It should apply replacements sequentially.
*   **Optimise `get_files_with_extension`:** Avoid walking/listing the same directory multiple times if multiple extensions are selected. Walk/list the directory once and then filter the results based on the selected extensions.
*   **Improve Logging:**
    *   Make logger configuration (app title, version, log file path) more dynamic or configurable.
    *   Add more detailed logging for errors and specific actions.
    *   Consider adding different log levels (DEBUG, INFO, WARNING, ERROR).
*   **Path Separators:** Use `os.path.join` consistently for constructing paths and `os.path.dirname` for getting parent directories to ensure cross-platform compatibility (Windows '' vs. Linux/macOS '/'). (`get_filepath_up` currently assumes '/').
*   **Hardcoded Values:** Avoid hardcoding values like `supported_files` directly in the code. Consider moving them to a configuration section or making them dynamically discoverable/user-configurable.

## Feature Enhancements

*   **Preview Changes:** Add a preview panel showing how filenames *will* look before executing the rename/copy operation.
*   **Undo Functionality:** Implement a mechanism to undo the last batch rename operation (might involve logging changes to a reversible format).
*   **Regular Expression Support:** Allow using regular expressions for find and replace.
*   **Case Sensitivity Option:** Add an option for find/replace operations to be case-sensitive or insensitive.
*   **More File Type Options:** Allow users to add/edit the list of supported file types directly in the UI, instead of just checkboxes for hardcoded types.
*   **Numbering/Sequencing:** Add options to sequentially number files (e.g., `image_001.png`, `image_002.png`).
*   **Progress Bar:** Implement a progress bar for long-running rename/copy operations, especially with recursion enabled.
*   **Drag and Drop:** Allow dragging a folder onto the application window to set the file path.

## UI/UX Improvements

*   **Clearer Button Text:** The main action button text ("Rename") should dynamically change to "Copy" if the copy method is selected.
*   **Disable Controls:** Disable the "Rename/Copy" button if no directory is selected or if essential parameters (like filetypes if filtering is on) are missing.
*   **Better Status Messages:** Provide more informative status messages (e.g., "Scanning files...", "Renaming file X of Y...", "Operation complete: X files renamed, Y errors.").
*   **UI Responsiveness:** For very large directories, perform file scanning and renaming in a separate thread to prevent the GUI from freezing. Use Qt's threading capabilities (`QThread`, signals/slots).

## Testing

*   **Unit Tests:** Create unit tests for functions in `batch_renamer_lib.py`, especially `get_renamed_file_path` and file discovery logic.

## Documentation

*   **Code Comments:** Add more detailed comments explaining complex logic within functions.
*   **README Update:** Keep the README updated as features are added or changed.
