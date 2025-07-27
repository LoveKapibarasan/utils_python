import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor
from pynput import keyboard

start_selection = threading.Event()

class AreaSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Area")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
        )
        self.setWindowState(Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.3)
        self.setCursor(Qt.CrossCursor)
        self.begin = self.end = None
        self.show()

    def paintEvent(self, event):
        if self.begin and self.end:
            painter = QPainter(self)
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            painter.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()
        self.print_region()

    def print_region(self):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        width = x2 - x1
        height = y2 - y1
        print(f"Selected region: {{'left': {x1}, 'top': {y1}, 'width': {width}, 'height': {height}}}")

def wait_for_hotkey():
    print("🔧 Press F8 when you're ready to select the area...")
    def on_press(key):
        if key == keyboard.Key.f8:
            print("🚀 F8 pressed — starting selection...")
            start_selection.set()
            return False  # Stop listener

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    threading.Thread(target=wait_for_hotkey).start()
    start_selection.wait()  # Wait for F8
    app = QApplication(sys.argv)
    selector = AreaSelector()
    sys.exit(app.exec_())
