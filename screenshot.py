import sys

from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QGuiApplication, QColor, QPainter, QPen, QPixmap


class CaptureScreen(QWidget):

    def __init__(self):
        self.full_screen_image: QPixmap = QPixmap()
        self.painter = QPainter()
        self.begin_position = None
        self.end_position = None
        self.is_mouse_press_left = False
        self.capture_image = None

        super().__init__()
        self.initWindow()
        self.captureFullScreen()

    def initWindow(self):
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)
        self.setWindowFlag(Qt.FramelessWindowHint)
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
            self.begin_position = event.pos()  # 记录选取区域开始的坐标
            self.is_mouse_press_left = True
        # if event.button() == Qt.RightButton:
        #     # 如果选取了图片,则按一次右键开始重新截图
        #     if self.capture_image is not None:
        #         self.capture_image = None
        #         # self.paintBackgroundImage()
        #         self.update()  # update的作用是调用paintEvent
        #     else:
        #         self.close()  # 关闭窗口

    def mouseMoveEvent(self, event):
        if self.is_mouse_press_left is True:
            self.end_position = event.pos()  # 选取区域结束坐标
            self.update()
            # self.repaint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_position = event.pos()
            self.repaint()
            self.is_mouse_press_left = False

    # def mouseDoubleClickEvent(self, event):
    #     if self.capture_image is not None:
    #         self.save_image()  # 保存截图图片
    #         self.close()  # 关闭窗口

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            if self.capture_image is not None:
                self.save_image(self.capture_image)  # 保存截图图片
                self.close()  # 关闭窗口

        if event.key() == Qt.Key_Escape:
            if self.capture_image is not None:
                self.capture_image = None
                # self.paintBackgroundImage()
                self.update()  # update的作用是调用paintEvent
            else:
                self.close()  # 关闭窗口

    # def save_image(self):
    #     self.capture_image.save("picture.png")
    def save_image(self, image):
        path, _ = QFileDialog.getSaveFileName(self, 'Save Image', './', 'File(*.png)')
        if path:
            image.save(path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaptureScreen()
    window.show()
    sys.exit(app.exec_())
