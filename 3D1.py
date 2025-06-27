from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                               QTextEdit, QGraphicsBlurEffect)
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPixmap, QPainter, QColor
import math
import time  # 新增时间模块用于精确计时
import wordsix
#30s 跳动版，查看如何实现的30s 跳动

class BouncingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("30秒周期物理弹跳动画")
        self.setGeometry(1300, 300, 800, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.init_controls()
        self.start_bounce_animation()
        self.word = wordsix.word_lists
        self.num = 0

    def init_controls(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 内容容器
        self.container = QWidget(self)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(20)

        # 文本框
        self.text_edit = QTextEdit(self.container)
        self.text_edit.setFixedSize(300, 60)
        self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 230);
            border: 1px solid rgba(0, 0, 0, 180);
            border-radius: 6px;
            padding: 8px;
        """)
        self.text_edit.setPlaceholderText("观察30秒完整跳动周期...")

        # 动画层
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

        # 物理参数配置（30秒完整周期）
        self.total_duration = 30000  # 30秒（毫秒）
        self.gravity = 0.0005  # 向下加速度
        self.elasticity = 0.8  # 弹性系数（0-1）
        self.amplitude = 150  # 最大跳动高度（像素）
        self.start_time = None
        self.current_height = 0

        # 初始位置
        self.text_bottom = self.text_edit.y() + self.text_edit.height()
        self.ground_level = self.height() - self.image_label.height() - 20
        self.start_pos = self.text_bottom + 20

        self.image_label.move(
            self.width() // 2 - self.image_label.width() // 2,
            self.start_pos
        )

        self.timer.start(16)  # 60FPS

    def update_bounce(self):
        if not self.start_time:
            self.start_time = time.time()  # 使用系统时间记录开始时刻

        elapsed = (time.time() - self.start_time) * 1000  # 转换为毫秒
        progress = elapsed / self.total_duration  # 0~1 之间的进度值

        # 使用缓动函数模拟真实弹跳
        if progress < 0.5:
            # 上升阶段（前15秒）
            self.current_height = self.amplitude * (1 - math.cos(progress * math.pi * 4)) ** 2
        else:
            # 下降阶段（后15秒）
            self.current_height = self.amplitude * (1 - math.cos(progress * math.pi * 4)) ** 2
            self.current_height *= self.elasticity ** ((progress - 0.5) * 2)

        # 计算新位置
        new_pos = self.start_pos - self.current_height
        clamped_pos = max(self.start_pos, min(new_pos, self.ground_level))

        # 更新位置
        self.image_label.move(
            self.image_label.x(),
            int(clamped_pos)
        )

        # 周期完成检测
        if elapsed > self.total_duration:
            self.start_time = None
            self.trigger_reset_effect()

    def trigger_reset_effect(self):
        """复位时的视觉反馈"""
        # 添加缩放动画
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

        # 添加文本框反馈
        self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 150, 230);
            border: 2px solid rgba(200, 200, 0, 180);
        """)
        QTimer.singleShot(300, lambda: self.text_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 230);
            border: 1px solid rgba(0, 0, 0, 180);
        """))

    def paintEvent(self, event):
        if self.isActiveWindow():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

    def resizeEvent(self, event):
        # 窗口缩放时更新位置
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
    window = BouncingWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec())