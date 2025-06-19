from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLabel,
)

from Pyside6.QtGui import QTextCursor

class TextEdit(QTextEdit):
    """
    编辑器自定义
    """
    def __init__(self):
        super().__init__()
        self.set_style()
        self.saved_cursor = None

    def set_style(self):
        self.setStyleSheet("""
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


class MainWindow(QMainWindow):
    """
    程序主界面
    """
    def __init__(self):
        super()
        self.init_ui()

    
    """s
    界面布局
    """
    def init_ui(self):
        self.setWindowTitle("文本表达式计算器")
        self.setGeometry(100, 100, 800, 600)

        # 编辑框
        self.text_edit = TextEdit()

        # 底部信息栏
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

    