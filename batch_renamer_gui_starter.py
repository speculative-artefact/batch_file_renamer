import sys
import os
import time
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# You'll need to make this ui in QtDesigner
# And convert it to a .py file using the MakeUIPy.bat file
from batch_renamer_ui import Ui_MainWindow

# Recommend you rename this
import batch_renamer_lib


class BatchRenamerWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # UI Setup
        super().__init__()
        super(Ui_MainWindow).__init__()
        self.setupUi(self)
        # Connect button to function
        self.push_button_browse_path.clicked.connect(self.get_filepath)
        self.push_button_up_dir.clicked.connect(self.get_filepath_up)
        # Update list when recursion or filetypes change
        self.check_box_recursion.clicked.connect(self.update_list)
        self.check_box_supported_filetypes.clicked.connect(self.update_list)
        # Switch find and replace strings
        self.push_button_switch_find_replace.clicked.connect(
            self.switch_find_and_replace
        )
        # Connect your new "Run" button to self.run_renamer
        self.push_button_rename.clicked.connect(self.run_renamer)
        # Instance the "back end"
        self.batch_renamer = batch_renamer_lib.BatchRenamer()

        # Variables
        self.supported_files = ["txt", "ma", "png"]

        # Show UI normal vs maximized
        self.showNormal()
        self.update_status("Ready")
        self.update_file_count("No directory selected")
        # Need to declare filepath as None
        # self.filepath = os.path.join( os.path.dirname ( __file__))

    def get_filepath(self):
        """
        Open a file dialog for browsing to a folder
        """
        self.filepath = QFileDialog().getExistingDirectory()
        self.set_filepath()

    def get_filepath_up(self):
        """
        Get parent directory of the current directory
        """
        num_of_dir = self.filepath.count("/")
        # Only go up if there are more than 1 directories
        if num_of_dir > 1:
            self.filepath = "/".join(self.filepath.split("/")[:-1])
            self.set_filepath()

    def set_filepath(self):
        """
        Set lineEdit text for filepath
        """
        self.line_edit_file_path.setText(self.filepath)
        self.update_list()

    def update_status(self, message):
        """
        Update status bar with message
        """
        self.label_action_status.setText(message)

    def update_file_count(self, message):
        """
        Update status bar with message
        """
        self.label_total_files.setText(message)

    def update_list(self):
        """
        Clear listwidget
        read files in filepath with os.walk
        Add files as new items
        Update total files label
        """
        # Files to be added to list widget
        files_to_add = []

        # Check if a directory has been selected
        if not self.filepath:
            self.update_file_count("No directory selected")
        else:
            self.list_widget_directory_browser.clear()
            if self.check_box_recursion.isChecked():
                # Recursively walk through the directory
                # and add files to the list widget
                for root, dirs, files in os.walk(self.filepath):
                    # NOTE: files is an arrary of an array of files
                    if self.check_box_supported_filetypes.isChecked():
                        # Only add supported filetypes
                        files_to_add += [
                            f
                            for f in files
                            if f.split(".")[-1] in self.supported_files
                            and os.path.isfile(os.path.join(root, f))
                        ]
                    else:
                        # Add all filetypes
                        files_to_add += files
            else:
                # Only add files from the selected directory
                for file in os.listdir(self.filepath):
                    # Only add files, excl. directories
                    if os.path.isfile(os.path.join(self.filepath, file)):
                        if self.check_box_supported_filetypes.isChecked():
                            # Only add supported filetypes
                            if file.split(".")[-1] in self.supported_files:
                                files_to_add.append(file)
                        else:
                            # Add all filetypes
                            files_to_add.append(file)

            # Add files to list widget
            self.list_widget_directory_browser.addItems(files_to_add)
            # update count total files label
            self.update_file_count(
                f"Total files: {self.list_widget_directory_browser.count()}"
            )

    def switch_find_and_replace(self):
        """
        Switch find and replace strings
        """
        find_string = self.line_edit_find_string.text()
        replace_string = self.line_edit_replace_string.text()
        self.line_edit_find_string.setText(replace_string)
        self.line_edit_replace_string.setText(find_string)

    # Add a function to gather and set parameters based upon UI
    # e.g. lineEdit.text() or radioButton.isChecked
    # remember that you may need to check to see if the result
    # was a tuple and correct like so:
    # self.filepath = self.line_edit_file_path.text()
    # if type(self.filepath) is tuple:
    #     self.filepath = self.filepath[0]

    def gather_rename_parameters(self):
        """
        Gather parameters for rename from UI
        """
        # clear filetypes list
        self.filetypes = []
        # get parameters from UI
        self.filepath = self.line_edit_file_path.text()
        if type(self.filepath) is tuple:
            self.filepath = self.filepath[0]
        self.copy_files = self.radio_button_method_copy.isChecked()
        self.filetypes_txt = self.check_box_filetypes_txt.isChecked()
        self.filetypes_ma = self.check_box_filetypes_ma.isChecked()
        self.filetypes_png = self.check_box_filetypes_png.isChecked()
        self.strings_to_find = self.line_edit_find_string.text()
        self.string_to_replace = self.line_edit_replace_string.text()
        self.prefix = self.line_edit_prefix.text()
        self.suffix = self.line_edit_suffix.text()
        self.recursion = self.check_box_recursion.isChecked()

        # Create a list of filetypes to pass to the batch_renamer
        if self.filetypes_txt:
            self.filetypes.append("txt")
        if self.filetypes_ma:
            self.filetypes.append("ma")
        if self.filetypes_png:
            self.filetypes.append("png")
        if not self.filetypes:
            # If no filetypes are selected, 
            # behave same as if all are selected
            self.filetypes = ["txt", "ma", "png"]

    def run_renamer(self):
        """
        Run back end batch renamer using self.batch_renamer
        self.batch_renamer is an instance of the BatchRenamer class
        """

        self.gather_rename_parameters()
        # Check if a directory has been selected
        if not self.filepath:
            self.QMessageBox = QMessageBox().critical(
                self,
                "No directory selected",
                "Please select a directory before running the renamer",
            )
        else:
            self.update_status("Renaming files")
            self.batch_renamer.rename_files_in_folder(
                self.filepath,
                self.filetypes,
                self.strings_to_find,
                self.string_to_replace,
                self.prefix,
                self.suffix,
                self.recursion,
                self.copy_files,
                self.update_status,
                self.update_list,
                QMessageBox(),
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BatchRenamerWindow()
    sys.exit(app.exec())
