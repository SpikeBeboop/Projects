from calc import Calc
from PySide6.QtWidgets import (
    QMainWindow, QWidget,QVBoxLayout,
    QTextEdit, QLabel
)

class MainWindow(QMainWindow):
    """
    程序主界面
    """
    def __init__(self):
        super().__init__()
        self._ignore_changes = False
        self.setui()
        self.handle()


    """
    页面初始化
    """
    def setui(self):
        # 窗口大小及标题
        self.setWindowTitle("文本表达式计算器")
        self.setGeometry(100,100,800,600)

        # 编辑框
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
                            QTextEdit {
                                border: none;
                                padding: 0px;
                                outline: none;
                            }
                            QTextEdit:focus {
                                border: none;
                                outline: none;
                            }
                        """)
        #底部信息栏
        self.label = QLabel("")

        # 布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle(self):
        self.text_edit.textChanged.connect(self.on_text_changed)

    """
    工具类
    """
    # 当文本被修改时
    def on_text_changed(self):
        if self._ignore_changes:
            return
        self._ignore_changes = True

        # 保存当前光标位置
        cursor = self.text_edit.textCursor()
        block = cursor.block()
        line_text = block.text().strip()
        self.calc(line_text)

        self._ignore_changes = False