from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                               QTextEdit, QMainWindow,QGraphicsBlurEffect)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QColor, QPainter

#这里使用图形实现了3D话，需要看下如何使用和实现

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 窗口基础设置
        self.setWindowTitle("Transparent Window Demo")
        self.setGeometry(300, 300, 800, 600)

        # 关键透明化设置
        self.setWindowFlag(Qt.FramelessWindowHint)  # 移除窗口边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 启用透明背景
        self.setStyleSheet("background: transparent;")  # 确保背景透明

        # 创建控件
        self.init_controls()

    def init_controls(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 创建透明图片容器
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("mla.jpeg").scaled(200, 200, Qt.KeepAspectRatio))
        self.image_label.setStyleSheet("background: transparent;")  # 图片背景透明

        # 创建半透明文本框
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 220);  # 半透明白色背景
            border: 1px solid rgba(0, 0, 0, 150);         # 半透明边框
            border-radius: 8px;
            padding: 10px;
        """)
        self.text_edit.setFixedHeight(120)

        # 添加控件到布局
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.text_edit, alignment=Qt.AlignCenter)

        # 添加浮动动画
        self.start_float_animation()

    def start_float_animation(self):
        """实现浮动动画效果"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_float)
        self.pos = 0
        self.timer.start(30)  # 约33FPS

    def update_float(self):
        """更新浮动位置"""
        self.pos += 0.5
        self.image_label.move(
            self.width() // 2 - self.image_label.width() // 2 + int(5 * abs(math.sin(self.pos / 10))),
            self.image_label.y()
        )

    def paintEvent(self, event):
        """自定义绘制事件（实现磨砂玻璃效果）"""
        if self.isActiveWindow():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # 创建模糊效果
            blur_radius = 15
            blur_effect = QGraphicsBlurEffect(self)
            blur_effect.setBlurRadius(blur_radius)

            # 截取屏幕内容
            screen_pixmap = QPixmap.grabWindow(QApplication.primaryScreen().virtualSibling().winId())

            # 应用模糊效果
            blurred_pixmap = QPixmap(screen_pixmap.size())
            blurred_pixmap.fill(Qt.transparent)
            painter.begin(blurred_pixmap)
            screen_pixmap.setGraphicsEffect(blur_effect)
            screen_pixmap.render(painter)
            painter.end()

            # 绘制模糊背景
            painter.drawPixmap(self.rect(), blurred_pixmap, self.rect())


if __name__ == "__main__":
    import sys
    import math
    #from PySide6.QtGui import QGraphicsBlurEffect

    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec())