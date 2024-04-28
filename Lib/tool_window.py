from .ui_tool_window import Ui_Tool_Window
from PyQt5 import QtWidgets,QtCore


class ToolWindow(Ui_Tool_Window, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ToolWindow()
    window.show()
    sys.exit(app.exec_())
