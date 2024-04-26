from Lib.screencapture_window import CaptureScreen
from Lib.tool_window import ToolWindow
from PyQt5 import QtWidgets
import sys


class Window(ToolWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_capture_button.clicked.connect(self.create_screencapture_window)
        self.screencapture_window: CaptureScreen = None

    def create_screencapture_window(self):
        self.screencapture_window = CaptureScreen()
        self.screencapture_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.move(1400, 900)
    window.show()
    sys.exit(app.exec_())
