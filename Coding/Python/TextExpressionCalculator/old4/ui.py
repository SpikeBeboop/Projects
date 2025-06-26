from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLabel,
)
from PySide6.QtGui import QTextCursor
from calc import Calculator

class TextEdit(QTextEdit):
    """
    编辑器自定义
    """

    def __init__(self):
        super().__init__()
        self.set_style()

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
        super().__init__()
        self.init()
        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """
        界面布局
        """
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

    def init(self):
        """
        初始化
        """
        self._ignore_changes = False
        self.saved_cursor = None
        self.calc = Calculator()

    def init_signals(self):
        """
        信号绑定
        """
        self.text_edit.textChanged.connect(self.handle_on_text_changed)
        self.calc.success.connect(self.handle_on_success)
        self.calc.error.connect(self.handle_on_error)

    def get_current_line_and_cursor(self):
        """
        获取当前行并保存光标
        """
        cursor = self.text_edit.textCursor()
        self.saved_cursor = QTextCursor(cursor)
        return cursor.block().text()

    def replace_current_line(self, new_line: str):
        """
        替换文本并恢复光标位置
        """
        if not self.saved_cursor:
            return
        cursor = QTextCursor(self.saved_cursor)
        block = cursor.block()
        column_offset = cursor.position() - block.position()

        cursor.beginEditBlock()
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(new_line)

        # 恢复光标位置
        new_pos = block.position() + min(column_offset, len(new_line))
        cursor.setPosition(new_pos)
        cursor.endEditBlock()
        self.text_edit.setTextCursor(cursor)

    """
    信号
    """
    def handle_on_text_changed(self):
        if self._ignore_changes:
            return
        current_line = self.get_current_line_and_cursor().strip()
        if current_line:
            self.calc.calculate(current_line)

    def handle_on_success(self, result: str):
        self._ignore_changes = True
        self.label.setText("")
        self.replace_current_line(result)
        self._ignore_changes = False

    def handle_on_error(self, error: str):
        """
        错误信号
        :param error:
        :return:
        """
        self.label.setText(error)
