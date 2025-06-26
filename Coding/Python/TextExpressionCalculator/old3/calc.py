# from itertools import count
#
# from PySide6.QtCore import QObject,Signal
# from asteval import Interpreter
# import re
#
# asteval = Interpreter()
#
# def aeval(expr:str)->str:
#     result = asteval(expr, raise_errors=True)
#     return str(result)
#
# class Calculator(QObject):
#     success = Signal(str)
#     error = Signal(str)
#
#
#     def __init__(self):
#         super().__init__()
#
#     def calculate(self, expr):
#         if expr=="": return
#         try:
#             self.success.emit(self.calc(expr))
#         except Exception:
#             self.error.emit(f"表达式错误")
#
#     def calc(self,expr):
#         if(self.is_number(expr)):
#             return expr
#         left, right = (expr.split('=', 1) + [''])[:2]
#         if all(not c.isdigit() for c in left) and self.is_number(right) and right != "":
#             aeval(expr)
#             return expr
#         result = aeval(left)
#         next = self.replace_first_number(right, str(result))
#         return f"{left}={self.calc(next)}"
#
#     def is_number(self,s):
#         return re.fullmatch(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s) is not None
#
#     def replace_first_number(self,expr: str, new_number: str) -> str:
#         if expr == "":
#             return new_number
#         return re.sub(r'\d+', new_number, expr, count=1)
#
#     def contain_operator(self, expr:str)->bool:
#         return any(op in expr for op in "+-*/%=")

from PySide6.QtCore import QObject, Signal
from asteval import Interpreter
import re

class Calculator(QObject):
    # 计算成功和失败的信号
    success = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.asteval = Interpreter()
        self.number_pattern = re.compile(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
        self.first_number_pattern = re.compile(r'\d+')

    def calculate(self, expr: str):
        """
        主入口，尝试计算表达式
        """
        if not expr.strip():
            return

        try:
            result = self.calc(expr.strip())
            self.success.emit(result)
        except Exception as e:
            self.error.emit("表达式错误")

    def calc(self, expr: str) -> str:
        """
        递归计算链式表达式，如 1+2=3*4=12
        """
        expr = expr.strip()

        # 表达式就是一个数值，直接返回
        if self.is_number(expr):
            return expr

        # 处理链式表达式
        left, right = (expr.split('=', 1) + [''])[:2]
        left = left.strip()
        right = right.strip()

        # 如果是变量赋值表达式，如 a=12
        if not any(c.isdigit() for c in left) and self.is_number(right):
            # 如果是新变量，添加到symtable
            self.asteval(left + '=' + right)  # 执行赋值
            return expr

        # 计算左侧
        result = self.eval_expr(left)

        # 替换右侧第一个数字为左侧结果，继续链式计算
        next_expr = self.replace_first_number(right, str(result))
        return f"{left}={self.calc(next_expr)}"

    def eval_expr(self, expr: str):
        """
        安全求值表达式
        """
        # 使用 asteval 进行计算，避免直接使用 eval
        value = self.asteval(expr, raise_errors=True)
        return value if value is not None else ""

    def is_number(self, s: str) -> bool:
        """
        判断是否为合法数值字符串
        """
        return bool(self.number_pattern.fullmatch(s.strip()))

    def replace_first_number(self, expr: str, new_number: str) -> str:
        """
        将表达式中第一个数字替换为新的数字
        """
        if not expr:
            return new_number
        return self.first_number_pattern.sub(new_number, expr, count=1)

    def contain_operator(self, expr: str) -> bool:
        """
        判断表达式是否包含运算符
        """
        return any(op in expr for op in "+-*/%=")