from PySide6.QtCore import QObject, Signal
from asteval import Interpreter
import re
import math

class Calculator(QObject):
    success = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.aeval = Interpreter()
        self.number_pattern = re.compile(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
        self.first_number_pattern = re.compile(r'\d+')
        self.variable_pattern = re.compile(r'[\u4e00-\u9fff_a-zA-Z][\u4e00-\u9fff\w]*')

        # 记录内置函数名
        self.builtin_names = set(self.aeval.symtable.keys())

        # 用内置的数学函数覆盖asteval中自带的sin、cos等三角函数
        self.aeval.symtable['sin'] = lambda x: math.sin(math.radians(x))  # 使用弧度制
        self.aeval.symtable['cos'] = lambda x: math.cos(math.radians(x))  # 使用弧度制
        self.aeval.symtable['tan'] = lambda x: math.tan(math.radians(x))  # 使用弧度制
        self.aeval.symtable['pi'] = math.pi
        self.aeval.symtable['e'] = math.e

    def check_forbidden_assignment(self, expr: str):
        """
        检查是否是非法赋值语句（如 sin=1），并且提示错误。
        """
        left, right = (expr.split('=', 1) + [''])[:2]
        left = left.strip()

        # 如果左侧为内置函数名，拒绝赋值
        if left in self.builtin_names:
            raise Exception(f"{left} 是内置函数名，不能赋值")

    def calculate(self, expr: str):
        """
        主入口，尝试计算表达式
        """
        expr = expr.strip()
        if not expr:
            return

        # 禁止处理增强赋值表达式，如 a+=1、总数-=2 等
        if re.search(r'[\u4e00-\u9fff_a-zA-Z]\w*\s*[\+\-\*/%]=', expr):
            return

        # 无操作符且不是变量名，不计算
        if not self.contain_operator(expr):
            if expr not in self.aeval.symtable:
                return
            # 是变量名，则触发输出变量值
            if callable(self.aeval.symtable[expr.strip()]):
                return
            result = self.aeval.symtable[expr]
            self.success.emit(f"{expr}={result}")
            return

        try:
            result = self.calc(expr)
            self.success.emit(result)
        except SyntaxError:
            self.error.emit("表达式错误")
        except ZeroDivisionError:
            self.error.emit("除数不能为0")
        except Exception:
            self.error.emit("表达式错误")

    def calc(self, expr: str) -> str:
        expr = expr.strip()

        # 处理三角函数
        if re.match(r'(sin|cos|tan)\(.*\)', expr):
            return f"{expr}={self.eval_expr(expr)}"

        if self.is_number(expr):
            return expr

        # 拆分等号
        left, right = (expr.split('=', 1) + [''])[:2]
        left = left.strip()
        right = right.strip()

        # 如果左边是合法变量名，视为赋值表达式
        if self.is_valid_variable(left):
            value = self.eval_expr(right)
            self.aeval.symtable[left] = value
            return f"{left}={value}"

        # 普通表达式
        result = self.eval_expr(left)
        if right:
            next_expr = self.replace_first_number(right, str(result))
            return f"{left}={self.calc(next_expr)}"
        else:
            return f"{left}={result}"

    def eval_expr(self, expr: str):
        """
        使用 asteval 安全求值
        """
        value = self.aeval(expr, raise_errors=True)
        return value if value is not None else ""

    def is_number(self, s: str) -> bool:
        return bool(self.number_pattern.fullmatch(s.strip()))

    def replace_first_number(self, expr: str, new_number: str) -> str:
        if not expr:
            return new_number
        return self.first_number_pattern.sub(new_number, expr, count=1)

    def is_valid_variable(self, name: str) -> bool:
        return bool(self.variable_pattern.fullmatch(name.strip()))

    def contain_operator(self, expr: str) -> bool:
        return any(op in expr for op in "+-*/%=")
