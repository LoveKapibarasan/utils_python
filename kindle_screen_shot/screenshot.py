import ctypes
import sys
import time
import os
import pyautogui
from PIL import ImageGrab
from PyQt6.QtGui import QIcon
from pywinauto.application import Application
from pywinauto import Desktop
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)


class ScreenshotAutomation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Screenshot Automation")
        self.setWindowIcon(QIcon("ico/screenshot.ico.png"))
        self.setGeometry(100, 100, 400, 300)

        self.target_window = None
        self.document_rect = None
        self.click_point = None

        self.launch_inspect()  # Launch inspect.exe at startup
        self.init_ui()


    def launch_inspect(self):
        """Launch inspect.exe with elevation (run as admin)."""
        inspect_path = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\inspect.exe"
        try:
            # Use ShellExecuteEx to run as administrator
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", inspect_path, None, None, 1)
            print("🔍 inspect.exe launched with admin rights.")
        except Exception as e:
            print(f"⚠️ Failed to launch inspect.exe: {e}")

    def init_ui(self):
        """Initialize GUI layout and widgets."""
        layout = QVBoxLayout()

        self.title_label = QLabel("Enter Window Title (prefix match):")
        self.title_input = QLineEdit()

        self.doc_label = QLabel("Enter Document Area Name:")
        self.doc_input = QLineEdit()

        self.button_label = QLabel("Enter Next Page Button Name:")
        self.button_input = QLineEdit()

        self.loop_label = QLabel("Enter Loop Count:")
        self.loop_input = QLineEdit()

        self.run_button = QPushButton("Start Capture")
        self.run_button.clicked.connect(self.run_process)

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.doc_label)
        layout.addWidget(self.doc_input)
        layout.addWidget(self.button_label)
        layout.addWidget(self.button_input)
        layout.addWidget(self.loop_label)
        layout.addWidget(self.loop_input)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def show_error(self, message):
        """Display error dialog."""
        QMessageBox.critical(self, "Error", message)

    def register_window(self, app_title):
        """Find target window by title."""
        print("🔍 Searching for target window...")

        windows = Desktop(backend="uia").windows()
        for w in windows:
            title = w.window_text()
            print("Available window lists: ", title)
            if app_title in title:
                print(f"✅ Target window found: {title}")
                app = Application(backend="uia").connect(handle=w.handle)
                self.target_window = app.window(handle=w.handle)
                return
        raise RuntimeError("Target window not found.")

    def register_ui(self, doc_name, button_name):
        """Find document area and next page button."""
        print("🔍 Searching for UI elements...")
        self.document_rect = None
        self.click_point = None
        for el in self.target_window.descendants():
            print("Available UI element lists: ", el.element_info.name)
            try:
                info = el.element_info
                name = info.name or ""
                rect = el.rectangle()

                # Detect document area
                if doc_name in name and self.document_rect is None:
                    self.document_rect = rect
                    print(f"📘 Document area detected: {rect}")

                # Detect next page button
                if name == button_name and self.click_point is None:
                    self.click_point = rect.mid_point()
                    print(f"➡️ Next page button detected: {self.click_point}")

            except Exception:
                continue

        if self.document_rect is None:
            raise RuntimeError("Document area not found.")
        if self.click_point is None:
            raise RuntimeError("Next page button not found.")

    def capture_loop(self, count):
        time.sleep(5)
        """Capture screenshots in loop and click to next page."""
        for i in range(count):
            print(f"🖼️ [{i + 1}] Capturing screenshot...")
            screenshot = ImageGrab.grab(bbox=(
                self.document_rect.left, self.document_rect.top,
                self.document_rect.right, self.document_rect.bottom
            ))
            os.makedirs("output", exist_ok=True)
            path = f"output/page_{i + 1:03}.png"
            screenshot.save(path)
            print(f"✅ Saved: {path}")

            print("🖱️ Clicking next page...")
            pyautogui.click(self.click_point.x, self.click_point.y)
            time.sleep(2)

        QMessageBox.information(self, "Done", "🎉 All screenshots captured!")

    def run_process(self):
        """Main procedure triggered by GUI button."""
        try:
            app_title = self.title_input.text().strip()
            doc_name = self.doc_input.text().strip()
            button_name = self.button_input.text().strip()
            loop_count = int(self.loop_input.text().strip())

            time.sleep(3)  # Allow time for window focus
            self.register_window(app_title)
            self.register_ui(doc_name, button_name)
            self.capture_loop(loop_count)

        except Exception as e:
            self.show_error(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotAutomation()
    window.show()
    sys.exit(app.exec())
