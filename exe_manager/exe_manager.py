# exe_manager.py
import sys
import csv
import os
import subprocess

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QInputDialog
)

SETTING_PATH = "setting.csv"

class ExeManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exe File Manager")
        self.setWindowIcon(QIcon("ico/exe_manager.ico"))
        self.resize(800, 400)
        self.data = []
        self.init_ui()
        self.load_csv()

    def init_ui(self):
        layout = QVBoxLayout()

        # Table for CSV data
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Path", "Name"])
        layout.addWidget(self.table)

        # Button layout
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")
        self.btn_select = QPushButton("Select .exe")
        self.btn_run = QPushButton("Run")
        self.btn_quit = QPushButton("Quit")

        for btn in [self.btn_add, self.btn_update, self.btn_delete, self.btn_select, self.btn_run, self.btn_quit]:
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Connect buttons to methods
        self.btn_add.clicked.connect(self.add_entry)
        self.btn_update.clicked.connect(self.update_entry)
        self.btn_delete.clicked.connect(self.delete_entry)
        self.btn_select.clicked.connect(self.select_exe)
        self.btn_run.clicked.connect(self.execute_exe)
        self.btn_quit.clicked.connect(self.close)

    def load_csv(self):
        if not os.path.exists(SETTING_PATH):
            return
        with open(SETTING_PATH, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            self.data = list(reader)
        self.refresh_table()

    def save_csv(self):
        with open(SETTING_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Path", "Name"])
            for row in self.data:
                writer.writerow(row)

    def refresh_table(self):
        self.table.setRowCount(len(self.data))
        for row_idx, row in enumerate(self.data):
            for col_idx, item in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(item))

    def get_selected_row(self):
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            return indexes[0].row()
        return None

    def add_entry(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .exe File", "", "Executable Files (*.exe)")
        if file_path:
            name = os.path.basename(file_path)
            new_id = str(len(self.data))
            self.data.append([new_id, file_path, name])
            self.refresh_table()
            self.save_csv()

    def update_entry(self):
        row = self.get_selected_row()
        if row is not None:
            file_path, _ = QFileDialog.getOpenFileName(self, "Update .exe File", "", "Executable Files (*.exe)")
            if file_path:
                name = os.path.basename(file_path)
                self.data[row] = [self.data[row][0], file_path, name]
                self.refresh_table()
                self.save_csv()

    def delete_entry(self):
        row = self.get_selected_row()
        if row is not None:
            del self.data[row]
            # Reassign IDs
            for idx, item in enumerate(self.data):
                item[0] = str(idx)
            self.refresh_table()
            self.save_csv()

    def select_exe(self):
        if not self.data:
            QMessageBox.information(self, "Info", "No data registered in the CSV.")
            return

        # Get the list of names
        exe_names = [row[2] for row in self.data]

        # Show selection dialog
        item, ok = QInputDialog.getItem(self, "Select Executable", "Select a registered .exe:", exe_names, editable=False)

        if ok and item:
            index = exe_names.index(item)
            self.table.selectRow(index)

    def execute_exe(self):
        row = self.get_selected_row()
        if row is not None:
            exe_path = self.data[row][1]
            exe_dir = os.path.dirname(exe_path)
            if os.path.exists(exe_path):
                try:
                    subprocess.Popen([exe_path], cwd=exe_dir)  # ★ Set working directory
                except Exception as e:
                    QMessageBox.warning(self, "Execution Error", str(e))
            else:
                QMessageBox.warning(self, "Error", f"File not found: {exe_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExeManager()
    window.show()
    sys.exit(app.exec_())

