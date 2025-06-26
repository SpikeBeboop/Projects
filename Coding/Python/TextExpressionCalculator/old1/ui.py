from calc import Calc
from PySide6.QtWidgets import (
QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget
)

class CalcUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setui()
        self.bandle()
        self._ignore_changes = False
        self.calc = Calc()


    def setui(self):
        self.setWindowTitle("文本表达式计算器")
        self.setGeometry(100, 100, 800, 600)

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
        self.label = QLabel("行：1, 列：1")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def bandle(self):
        #self.text_edit.cursorPositionChanged.connect(self.on_cusor_position_changed)
        self.text_edit.textChanged.connect(self.on_text_changed)

    def on_cusor_position_changed(self):
        cursor = self.text_edit.textCursor()
        block = cursor.block()  # 获取当前行（段）
        line = block.blockNumber() + 1
        column = cursor.positionInBlock() + 1  # 当前行内的位置
        self.label.setText(f"行: {line}，列: {column}")

    def on_text_changed(self):
        if self._ignore_changes:
            return

        self._ignore_changes = True

        # 保存当前光标位置
        cursor = self.text_edit.textCursor()
        cur_line = cursor.blockNumber()
        cur_col = cursor.positionInBlock()

        block = cursor.block()
        line_text = block.text().strip()
        self.expression_judgment(line_text)

        self._ignore_changes = False

    def print_on_label(self, string:str):
        self.label.setText(string)

    def expression_judgment(self, content:str):
        if any(c.isdigit for c in content):
            resault = self.calc(content)
            print(resault)
