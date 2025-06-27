from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QMainWindow,QTextEdit
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
import random
import sys
import word
import time


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.vy = 0          # 垂直速度
        self.gravity = 0.5    # 重力加速度
        self.jump_power = -15 # 跳跃力度
        self.is_jumping = False
        self.base_y = 0       # 基准Y坐标（文本框下方）
        self.setAttribute(Qt.WA_DeleteOnClose)  # 关闭时自动销毁对象


    def initUI(self):
        self.setWindowTitle('text')
        self.setGeometry(1700, 800, 100, 100)  # 设置窗口位置和大小
        #self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #F0E68C;")  # 设置背景颜色

        # 创建布局管理器
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 创建标签用于显示宠物图片
        self.pet_label = QLabel(self)
        self.picture = QPixmap("mla.jpeg")
        # 计算新的尺寸，例如宽度和高度都缩小到原来的100%
        width = self.picture.width() // 100
        height = self.picture.height() // 100
        # 缩放图片
        pixmap = self.picture.scaled(width, height, Qt.KeepAspectRatio)
        self.pet_label.setPixmap(pixmap )  # 设置宠物图片路径
        self.pet_label.move(50, 50)  # 初始位置

        # 创建文本框
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
             background-color: white;
             border: 1px solid #CCCCCC;
             border-radius: 5px;
             padding: 5px;
         """)
        self.text_edit.setFixedHeight(40)  # 设置固定高度
        layout.addWidget(self.text_edit)
        layout.addWidget(self.pet_label, alignment=Qt.AlignTop)
        # 初始化宠物位置（文本框下方居中）
        self.base_y = self.text_edit.y() + self.text_edit.height() + 10
        self.pet_label.move(
            (self.width() - self.pet_label.width()) // 2,
            self.base_y
        )

        # 创建定时器，用于更新up
        self.timerup = QTimer(self)
        self.timerup.timeout.connect(self.upPet)
        #self.timer.timeout.connect(self.updatePetPosition)
        self.timerup.start(1000)  # 每100毫秒移动一次
        #创建定时器，用于down
        self.timerd = QTimer(self)
        self.timerd.timeout.connect(self.downPet)
        # self.timer.timeout.connect(self.updatePetPosition)
        self.timerd.start(1010)  # 每100毫秒移动一次

    def upPet(self):
        # 获取当前位置
        x = self.pet_label.x()
        #y = self.pet_label.y()
        y = self.text_edit.y() + self.text_edit.height() + 15
        print('up up up x is {} y is {}'.format(x, y))
        self.pet_label.move(x, y)
        # 计算新位置，简单地在窗口内随机移动
        new_x = x + (random.randint(-40, 40))
        #new_y = y + (random.randint(-5, 0))
        #time.sleep(10)
        #new_x = x
        new_y = y - 15
        # 确保宠物不会移出窗口外
        if new_x < 0: new_x = 0
        if new_y < 0: new_y = 0
        print('the width is {} and pet_label  width is {}'.format( self.width(), self.pet_label.width()))
        if new_x + self.pet_label.width() > self.width(): new_x = self.width() - self.pet_label.width()/2
        #if new_y + self.pet_label.height() > self.height(): new_y = self.height() - self.pet_label.height()
        # 移动宠物到新位置
        print('up up up x is {} y is {}'.format(new_x, new_y))
        self.pet_label.move(new_x, new_y)
        self.update_text_box()

    def downPet(self):
        # 获取当前位置
        self.pet_label.move(
            self.pet_label.x(),
            self.base_y
        )

    def update_text_box(self):
        """更新文本框内容"""
        current_text = self.text_edit.toPlainText()
        # 显示宠物坐标和word.word_n内容（假设word.py存在且包含word_n列表）
        new_line = 'hello word'
        self.text_edit.setText(current_text + new_line)
        # 自动滚动到底部
        self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

    def closeEvent(self, event):
        """窗口关闭时停止定时器"""
        self.timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PetWindow()
    #设置窗口属性，使窗口一直置于top层
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec())