from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                               QTextEdit, QSpinBox, QHBoxLayout)
from PySide6.QtCore import Qt, QTimer, QPoint, QEvent
from PySide6.QtGui import QPixmap, QPainter, QColor, QMouseEvent
import math
import time

#废物版
class DraggableLabel(QLabel):
    """可拖拽的标签类，支持边界检测和Z轴控制"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_start = None
        self.offset = QPoint()
        self.setMouseTracking(True)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start = event.globalPosition().toPoint()
            self.offset = self.mapToParent(event.position().toPoint())
            self.parent().animation_paused = True  # 暂停动画
            self.raise_()  # 置顶图层

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and self.drag_start is not None:
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self.drag_start

            # 计算新位置（带边界限制）
            new_pos = self.mapToParent(self.offset) + delta
            max_x = self.parent().width() - self.width() - 20
            max_y = self.parent().height() - self.height() - 20

            new_pos.setX(max(20, min(new_pos.x(), max_x)))
            new_pos.setY(max(20, min(new_pos.y(), max_y)))

            self.move(new_pos)
            self.drag_start = current_pos

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start = None
            self.parent().animation_paused = False  # 恢复动画


class BouncingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.animation_paused = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("可交互弹跳动画")
        self.setGeometry(1300, 300, 800, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.init_controls()
        self.init_animation()

    def init_controls(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 控制面板
        control_panel = QWidget(self)
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(10)

        # 周期设置
        self.period_spin = QSpinBox(control_panel)
        self.period_spin.setRange(1, 300)  # 1秒到5分钟
        self.period_spin.setValue(30)  # 默认30秒
        self.period_spin.setSuffix("秒周期")
        self.period_spin.valueChanged.connect(self.set_animation_period)

        control_layout.addWidget(self.period_spin)
        main_layout.addWidget(control_panel, alignment=Qt.AlignRight)

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
        self.text_edit.setPlaceholderText("拖拽图像并调整周期...")

        # 可交互图像
        self.image_label = DraggableLabel(self.container)
        self.image_label.setPixmap(QPixmap("mla.jpeg").scaled(
            80, 80,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.image_label.setStyleSheet("background: transparent;")

        container_layout.addWidget(self.text_edit)
        container_layout.addWidget(self.image_label)

        main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

    def init_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.set_animation_period(30)  # 初始化周期

    def set_animation_period(self, seconds):
        """设置动画周期（秒）"""
        self.animation_period = seconds * 1000  # 转换为毫秒
        self.reset_animation()

    def reset_animation(self):
        """重置动画参数"""
        self.start_time = time.time()
        self.text_bottom = self.text_edit.y() + self.text_edit.height()
        self.start_pos = self.text_bottom + 20
        self.ground_level = self.height() - self.image_label.height() - 20

        # 保持当前拖拽位置
        current_pos = self.image_label.pos()
        self.image_label.move(
            current_pos.x(),
            self.start_pos
        )

    def update_animation(self):
        if self.animation_paused:
            return

        elapsed = (time.time() - self.start_time) * 1000
        progress = elapsed / self.animation_period

        # 物理计算
        if progress < 0.5:
            self.current_height = 150 * (1 - math.cos(progress * math.pi * 4)) ** 2
        else:
            self.current_height = 150 * (1 - math.cos(progress * math.pi * 4)) ** 2
            self.current_height *= 0.8 ** ((progress - 0.5) * 2)

        # 位置更新（保持拖拽后的水平位置）
        new_pos = QPoint(
            self.image_label.x(),
            self.start_pos - self.current_height
        )
        clamped_pos = QPoint(
            new_pos.x(),
            max(self.start_pos, min(new_pos.y(), self.ground_level))
        )

        self.image_label.move(clamped_pos)

        # 周期重置检测
        if elapsed > self.animation_period:
            self.start_time = time.time()
            self.trigger_reset_effect()

    def trigger_reset_effect(self):
        """周期结束时的视觉反馈"""
        # 缩放动画
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

        # 文本框反馈
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
        # 窗口缩放时更新地面位置
        self.ground_level = self.height() - self.image_label.height() - 20


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = BouncingWindow()
    window.show()
    sys.exit(app.exec())