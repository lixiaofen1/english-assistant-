from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                               QTextEdit, QGraphicsBlurEffect)
from PySide6.QtCore import Qt, QTimer, QPoint, QEvent
from PySide6.QtGui import QPixmap, QPainter, QColor, QMouseEvent
import math
import wordsix

#这里实现了图像的顶层显示和可拖拽话

class BouncingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_dragging = False
        self.drag_start_position = QPoint()
        self.window_start_position = QPoint()
        self.word =wordsix.word_lists
        self.num = 0

    def initUI(self):
        # 窗口基础设置
        self.setWindowTitle("全能悬浮动画窗口")
        self.setGeometry(1300, 300, 500, 350)

        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        # 初始化控件
        self.init_controls()
        self.start_bounce_animation()

    def init_controls(self):
        # 主布局容器
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 内容容器
        self.container = QWidget(self)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(20)

        # 文本框（可编辑）
        self.text_edit = QTextEdit(self.container)
        self.text_edit.setFixedSize(300, 60)
        self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 230);
            border: 1px solid rgba(0, 0, 0, 180);
            border-radius: 6px;
            padding: 8px;
        """)
        self.text_edit.setPlaceholderText("可编辑文本框...")

        # 动画元素
        self.image_label = QLabel(self.container)
        self.image_label.setPixmap(QPixmap("mla.jpeg").scaled(
            80, 80,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.image_label.setStyleSheet("background: transparent;")

        container_layout.addWidget(self.text_edit)
        container_layout.addWidget(self.image_label)

        main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

    def start_bounce_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bounce)

        # 动画参数配置
        self.gravity = 0.15
        self.velocity = 0
        self.amplitude = 40
        self.phase = 3 * math.pi / 2  # 初始相位（从下方开始）

        # 位置计算
        self.text_bottom = self.text_edit.y() + self.text_edit.height()
        self.start_pos = self.text_bottom + 20
        self.ground_level = self.height() - self.image_label.height() - 20

        # 初始化位置
        self.image_label.move(
            self.width() // 2 - self.image_label.width() // 2,
            self.start_pos
        )

        self.timer.start(16)

    def update_bounce(self):
        # 正弦波运动计算
        #原始参数0.1 这里和time start可以互相调试，time长的话，这里要短
        self.phase += 0.1
        new_pos = self.start_pos - self.amplitude * math.sin(self.phase)

        # 位置限制
        clamped_pos = max(self.start_pos, min(new_pos, self.ground_level))

        # 更新位置
        self.image_label.move(
            self.image_label.x(),
            int(clamped_pos)
        )

        # 周期结束检测
        if self.phase > 2 * math.pi:
            self.phase = 0
            self.trigger_reset_effect()

    def trigger_reset_effect(self):
        """周期结束时的视觉反馈"""
        # 动画缩放效果
        self.image_label.setPixmap(
            QPixmap("mla.jpeg").scaled(
                85, 85,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        QTimer.singleShot(100, lambda: self.image_label.setPixmap(
            QPixmap("mla.jpeg").scaled(
                80, 80,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        ))

        # 文本框颜色反馈
        self.update_text_box()
        self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 150, 230);
            border: 2px solid rgba(200, 200, 0, 180);
        """)
        QTimer.singleShot(300, lambda: self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 230);
            border: 1px solid rgba(0, 0, 0, 180);
        """))


    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件处理"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_position = event.globalPosition().toPoint()
            self.window_start_position = self.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件处理"""
        if self.is_dragging and event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_start_position
            self.move(self.window_start_position + delta)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件处理"""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            event.accept()

    def paintEvent(self, event):
        """绘制透明背景"""
        if self.isActiveWindow():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

    def resizeEvent(self, event):
        """窗口缩放时更新布局"""
        self.text_bottom = self.text_edit.y() + self.text_edit.height()
        self.start_pos = self.text_bottom + 20
        self.ground_level = self.height() - self.image_label.height() - 20
        self.image_label.move(
            self.image_label.x(),
            self.start_pos
        )

    def update_text_box(self):
        """更新文本框内容"""
        current_text = self.text_edit.toPlainText()
        self.num += 1
        new_line = self.word['日常口语'][self.num]
        self.text_edit.setText(new_line)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # 可选：设置全局样式
    app.setStyleSheet("""
        QTextEdit {
            border: 1px solid rgba(0, 0, 0, 180);
            border-radius: 6px;
        }
        QTextEdit:focus {
            border: 2px solid rgba(0, 120, 215, 200);
        }
    """)

    window = BouncingWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec())