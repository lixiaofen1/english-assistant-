from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                               QTextEdit, QGraphicsBlurEffect,QMenu)
from PySide6.QtCore import Qt, QTimer, QPoint, QEvent
from PySide6.QtGui import QPixmap, QPainter, QColor, QMouseEvent,QCursor
import math
#导入单词表
import wordtree, wordsix,wordnine,bussionword,workcolloword,softwareword,codeword,newword


#这里实现了图像的顶层显示和可拖拽话
#软件目标，主打背不下来也要留下一个印象。背单词是痛苦的，但是留下个印象，在反复加深是简单的

class BouncingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_dragging = False
        self.drag_start_position = QPoint()
        self.window_start_position = QPoint()
        self.num = 0
        self.createContextMenu()
        #单词初始化部分 （初阶）3000 （中阶）6000 （高阶）9000 商务 工作口语 软件工程单词 程序员单词 新闻单词
        self.wordtree = wordtree.wordtree_list
        self.wordsix = wordsix.wordsix_lists
        self.wordnine = wordnine.wordnine_list
        self.wordbusi = bussionword.business_terms_combined
        self.wordwork = workcolloword.workcllowordlist
        self.wordsoft = softwareword.software_engineering_words
        self.wordcode = codeword.codeowrdlist
        self.wordnew = newword.news_vocabulary
        self.wordall = ['右键点击图像（左下角）进行开始']
        self.flagchange = 0
        #跳动频率
        self.fruquency_num = 2


    def initUI(self):
        # 窗口基础设置
        self.setWindowTitle("单词跳动")
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
        #self.fruquency_num

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
        #if self.phase > 2 * math.pi:
        if self.phase > self.fruquency_num * math.pi:
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
        #current_text = self.text_edit.toPlainText()
        if(self.flagchange):
            self.num = 0
            self.flagchange = 0
        try:
            new_line = self.wordall[self.num]
            self.text_edit.setText(str(new_line))
            self.num += 1
        except  Exception as e:
            self.num =0


    def createContextMenu(self):
        '''''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        #tree
        self.action_tree = self.contextMenu.addAction(u'跳动3000初阶词')
        self.action_tree.triggered.connect(self.actionHandler_action_tree)
        #six
        self.action_six = self.contextMenu.addAction(u'跳动3000中阶词')
        self.action_six.triggered.connect(self.actionHandler_action_six)
        #nine
        self.action_nine = self.contextMenu.addAction(u'跳动3000高阶词')
        self.action_nine.triggered.connect(self.actionHandler_action_nine)
        #busi
        self.action_busi = self.contextMenu.addAction(u'跳动business word')
        self.action_busi.triggered.connect(self.actionHandler_action_busi)
        #work
        self.action_work = self.contextMenu.addAction(u'跳动work place word')
        self.action_work.triggered.connect(self.actionHandler_action_work)
        #soft
        self.action_soft = self.contextMenu.addAction(u'跳动software word')
        self.action_soft.triggered.connect(self.actionHandler_action_soft)
        #code
        self.action_code = self.contextMenu.addAction(u'跳动code word')
        self.action_code.triggered.connect(self.actionHandler_action_code)
        #new
        self.action_new = self.contextMenu.addAction(u'跳动News word')
        self.action_new.triggered.connect(self.actionHandler_action_new)
        #all
        self.action_all = self.contextMenu.addAction(u'教练我要滚全部的单词')
        self.action_all.triggered.connect(self.actionHandler_action_all)
        #跳动频率正常
        self.action_normal = self.contextMenu.addAction(u'跳动正常')
        self.action_normal.triggered.connect(self.actionHandler_action_normal)
        # 跳动频率变慢
        self.action_slow = self.contextMenu.addAction(u'跳动变慢')
        self.action_slow.triggered.connect(self.actionHandler_action_slow)
        # 作者信息
        self.action_author = self.contextMenu.addAction(u'作者信息')
        self.action_author.triggered.connect(self.actionHandler_action_author)

    def showContextMenu(self, pos):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QCursor().pos())
        # self.contextMenu.move(QtGui.)
        self.contextMenu.show()

    def actionHandler_action_author(self):
        self.flagchange = 1
        self.wordall = ['公众号：搞个项目\n作者信息：Tom\n请作者喝个蜜雪']

    def actionHandler_action_normal(self):
        self.fruquency_num = 2

    def actionHandler_action_slow(self):
        self.fruquency_num = 8

    def actionHandler_action_tree(self):
        self.flagchange = 1
        self.wordall = self.wordtree

    def actionHandler_action_six(self):
        self.flagchange = 1
        self.wordall = self.wordsix

    def actionHandler_action_nine(self):
        self.flagchange = 1
        self.wordall = self.wordnine

    def actionHandler_action_busi(self):
        self.flagchange = 1
        self.wordall = self.wordbusi

    def actionHandler_action_work(self):
        self.flagchange = 1
        self.wordall = self.wordwork

    def actionHandler_action_soft(self):
        self.flagchange = 1
        self.wordall = self.wordsoft

    def actionHandler_action_code(self):
        self.flagchange = 1
        self.flagchange = 1
        self.wordall = self.wordcode

    def actionHandler_action_new(self):
        self.flagchange = 1
        self.wordall =  self.wordnew

    def actionHandler_action_all(self):
        #加载全部的list 如何组装list
        self.flagchange = 1
        self.wordall = self.wordtree



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
        QMenu {
            background-color: white;  /* 设置背景颜色 */
            color: white;            /* 设置文字颜色 */
        }
        QMenu::item:selected {
            background-color: lightblue; /* 设置选中项的背景颜色 */
        }
    """)


    window = BouncingWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec())