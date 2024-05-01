from typing import Optional

from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QGuiApplication, QColor, QPainter, QPen, QPixmap


class CaptureScreen(QWidget):
    def __init__(self, *args, **kwargs):
        self.full_screen_image: Optional[QPixmap] = None
        self.painter: QPainter = QPainter()
        self.begin_position = None
        self.end_position = None
        self.is_mouse_press_left: bool = False
        self.capture_image: Optional[QPixmap] = None
        self.window_hint_capture_screen: Optional[HintCaptureScreen] = None

        super().__init__(*args, **kwargs)
        self.initWindow()
        self.captureFullScreen()

    def initWindow(self):
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)

    def captureFullScreen(self):
        self.full_screen_image = QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

    def paintBackgroundImage(self):
        shadow_color = QColor(0, 0, 0, 100)
        self.painter.drawPixmap(0, 0, self.full_screen_image)
        self.painter.fillRect(self.full_screen_image.rect(), shadow_color)

    def getRectangle(self, begin_point, end_point):
        pick_rect_width = int(abs(begin_point.x() - end_point.x()))
        pick_rect_height = int(abs(begin_point.y() - end_point.y()))
        pick_rect_begin_point_x = begin_point.x() if begin_point.x() < end_point.x() else end_point.x()
        pick_rect_begin_point_y = begin_point.y() if begin_point.y() < end_point.y() else end_point.y()
        pick_rect = QRect(pick_rect_begin_point_x, pick_rect_begin_point_y, pick_rect_width, pick_rect_height)
        # 避免高度宽度为0时候报错
        if pick_rect_width == 0:
            pick_rect.setWidth(2)
        if pick_rect_height == 0:
            pick_rect.setHeight(2)

        return pick_rect

    def paintEvent(self, event):
        self.painter.begin(self)
        self.paintBackgroundImage()
        pen_color = QColor(30, 144, 245)
        self.painter.setPen(QPen(pen_color, 1, Qt.SolidLine, Qt.RoundCap))
        if self.is_mouse_press_left is True:
            pick_rect = self.getRectangle(self.begin_position, self.end_position)
            self.capture_image = self.full_screen_image.copy(pick_rect)
            self.painter.drawPixmap(pick_rect.topLeft(), self.capture_image)
            self.painter.drawRect(pick_rect)
        self.painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin_position = event.pos()
            self.is_mouse_press_left = True

    def mouseMoveEvent(self, event):
        if self.is_mouse_press_left is True:
            self.end_position = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_position = event.pos()
            self.repaint()
            self.is_mouse_press_left = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            if self.capture_image is not None:
                self.save_image(self.capture_image)
                self.close()

        if event.key() == Qt.Key_T:
            if self.capture_image is not None:
                self.window_hint_capture_screen = HintCaptureScreen(image=self.capture_image)
                self.window_hint_capture_screen.show()
                self.close()

        if event.key() == Qt.Key_Escape:
            if self.capture_image is not None:
                self.capture_image = None
                self.update()  # update的作用是调用paintEvent
            else:
                self.close()

    def save_image(self, image):
        path, _ = QFileDialog.getSaveFileName(self, 'Save Image', './', 'File(*.png)')
        if path:
            image.save(path)


class HintCaptureScreen(QWidget):
    def __init__(self, parent: Optional[CaptureScreen] = None, flag=Qt.WindowFlags(), image: Optional[QPixmap] = None):
        self.painter = QPainter()
        self.parent = parent
        self.image = image
        self.start_x = None
        self.start_y = None

        super().__init__(parent, flag)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(image.width(), image.height())

    def initImage(self, image):
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, image)
        self.painter.end()

    def paintEvent(self, event):
        self.initImage(self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseMoveEvent(self, event):
        if not self.start_x or not self.start_y:
            return

        dis_x = event.x() - self.start_x
        dis_y = event.y() - self.start_y
        self.move(self.x() + dis_x, self.y() + dis_y)

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = CaptureScreen()
    window.show()

    sys.exit(app.exec_())
