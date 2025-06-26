# from PySide6.QtWidgets import (
#     QMainWindow, QWidget,QVBoxLayout,
#     QTextEdit, QLabel
# )
# from PySide6.QtGui import QTextCursor
# from calc import Calculator
#
# class MainWindow(QMainWindow):
#     """
#     程序主界面
#     """
#     def __init__(self):
#         super().__init__()
#         self.initui()
#         self.handle()
#
#
#     """
#     页面初始化
#     """
#     def initui(self):
#         #成员注册
#         self._ignore_changes = False
#         self.calculator = Calculator()
#
#         # 窗口大小及标题
#         self.setWindowTitle("文本表达式计算器")
#         self.setGeometry(100,100,800,600)
#
#         # 编辑框
#         self.text_edit = QTextEdit()
#         self.text_edit.setStyleSheet("""
#                             QTextEdit {
#                                 border: none;
#                                 padding: 0px;
#                                 outline: none;
#                             }
#                             QTextEdit:focus {
#                                 border: none;
#                                 outline: none;
#                             }
#                         """)
#         #底部信息栏
#         self.label = QLabel("")
#
#         # 布局
#         layout = QVBoxLayout()
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)
#         layout.addWidget(self.text_edit)
#         layout.addWidget(self.label)
#
#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)
#
#     def handle(self):
#         self.text_edit.textChanged.connect(self.on_text_changed)
#
#         self.calculator.success.connect(self.on_success)
#         self.calculator.error.connect(self.on_error)
#
#
#     """
#     工具类
#     """
#     def on_success(self, result:str):
#         if self._ignore_changes:
#             return
#         self._ignore_changes = True
#         self.label.setText("")
#         cursor = QTextCursor(self.saved_cursor)
#         cursor.beginEditBlock()
#         block_position=cursor.block().position()
#         column_offset = self.saved_cursor.position()-block_position
#
#         cursor.select(QTextCursor.SelectionType.LineUnderCursor)
#         cursor.removeSelectedText()
#         cursor.insertText(result)
#
#         new_pos=cursor.block().position()+min(column_offset, len(result))
#         cursor.setPosition(new_pos)
#         cursor.endEditBlock()
#         self.text_edit.setTextCursor(cursor)
#
#     def on_error(self, error:str):
#         self.label.setText(error)
#
#     # 当文本被修改时
#     def on_text_changed(self):
#         if self._ignore_changes:
#             return
#         cursor = self.text_edit.textCursor()
#         self.saved_cursor=QTextCursor(cursor)
#         block = cursor.block()
#         current_line = block.text()
#         self.calculator.calculate(current_line)
#         self._ignore_changes = False




from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLabel
)
from PySide6.QtGui import QTextCursor
from calc import Calculator


class MainWindow(QMainWindow):
    """
    程序主界面
    """
    def __init__(self):
        super().__init__()
        self._ignore_changes = False
        self.saved_cursor = None
        self.calculator = Calculator()

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """
        页面初始化
        """
        self.setWindowTitle("文本表达式计算器")
        self.setGeometry(100, 100, 800, 600)

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

    def init_signals(self):
        """
        信号绑定
        """
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.calculator.success.connect(self.on_success)
        self.calculator.error.connect(self.on_error)

    def on_success(self, result: str):
        """
        成功回调，替换当前行文本为计算结果并复原光标位置
        """
        if self._ignore_changes or not self.saved_cursor:
            return

        self._ignore_changes = True
        self.label.clear()

        cursor = QTextCursor(self.saved_cursor)
        block = cursor.block()
        column_offset = cursor.position() - block.position()

        cursor.beginEditBlock()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(result)

        # 恢复光标位置
        new_pos = block.position() + min(column_offset, len(result))
        cursor.setPosition(new_pos)
        cursor.endEditBlock()
        self.text_edit.setTextCursor(cursor)

        self._ignore_changes = False

    def on_error(self, error: str):
        """
        错误回调
        """
        self.label.setText(error)

    def on_text_changed(self):
        """
        当文本修改时，获取当前行文本并计算
        """
        if self._ignore_changes:
            return

        cursor = self.text_edit.textCursor()
        self.saved_cursor = QTextCursor(cursor)  # 保存当前光标

        current_line = cursor.block().text().strip()
        if current_line:  # 避免空行计算
            self.calculator.calculate(current_line)
