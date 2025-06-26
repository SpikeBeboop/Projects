from PySide6.QtWidgets import QApplication, QPlainTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
import re
import sys
import math

class VariableCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("变量表达式计算器")
        self.editor = QPlainTextEdit()
        self.editor.setPlainText("$a = 2 + 3\n$a * 2\n$a * 2 + 1")
        self.editor.textChanged.connect(self.on_text_changed)
        self._ignore_changes = False

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def build_variable_table(self, lines):
        """构建变量表"""
        var_table = {}
        for line in lines:
            match = re.match(r"^\s*(\$\w+)\s*=\s*(.+?)(?:\s*=\s*\d+)?\s*$", line)
            if match:
                var, expr = match.groups()
                expr = self.replace_variables(expr.strip(), var_table)
                try:
                    value = eval(expr, {"__builtins__": {}}, vars(math))
                    var_table[var] = value
                except:
                    pass
        return var_table

    def replace_variables(self, expr, var_table):
        return re.sub(r"\$\w+", lambda m: str(var_table.get(m.group(0), m.group(0))), expr)

    def evaluate_and_append(self, line, var_table):
        """无论是否包含等号，都计算表达式并追加结果"""
        match = re.match(r"^\s*(.+?)\s*(?:=\s*.*)?$", line.strip())
        if not match:
            return line
        expr = match.group(1)
        expr_eval = self.replace_variables(expr, var_table)

        try:
            result = eval(expr_eval, {"__builtins__": {}}, vars(math))
            return f"{expr} = {result}"
        except:
            return line  # 错误则返回原样

    def on_text_changed(self):
        if self._ignore_changes:
            return

        self._ignore_changes = True

        # 保存当前光标位置
        cursor = self.editor.textCursor()
        cur_line = cursor.blockNumber()
        cur_col = cursor.positionInBlock()

        lines = self.editor.toPlainText().splitlines()
        var_table = self.build_variable_table(lines)

        new_lines = []
        for line in lines:
            if not line.strip():
                new_lines.append("")
                continue
            updated = self.evaluate_and_append(line, var_table)
            new_lines.append(updated)

        self.editor.blockSignals(True)
        self.editor.setPlainText("\n".join(new_lines))
        self.editor.blockSignals(False)

        # 恢复光标
        new_cursor = self.editor.textCursor()
        new_cursor.movePosition(QTextCursor.Start)
        for _ in range(cur_line):
            new_cursor.movePosition(QTextCursor.Down)
        new_cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, cur_col)
        self.editor.setTextCursor(new_cursor)

        self._ignore_changes = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VariableCalculator()
    win.resize(700, 400)
    win.show()
    sys.exit(app.exec())
