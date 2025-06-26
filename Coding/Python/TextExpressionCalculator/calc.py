import re
import math
from asteval import Interpreter
from PySide6.QtCore import QObject, Signal

aeval = Interpreter()

class Calculator(QObject):
    success = Signal(str)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.func_calls_pattern=re.compile(r'^([\u4e00-\u9fa5a-zA-Z_]+)\((.+)\)$')

        #自定义函数列表
        self.functions = {
            'sin': lambda x: math.sin(math.radians(x)),
            'cos': lambda x: math.cos(math.radians(x)),
            'tan': lambda x: math.tan(math.radians(x)),
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log
        }
        # 常量列表
        self.constants = [
            'pi','e'
        ]
        #变量列表
        self.variables = {
            'pi': math.pi,
            'e': math.e
        }
    """
    主业务类
    """
    def calculate(self, expr:str):
        expression,sep,right = expr.partition('#')
        expr = expression.strip()
        if not expr:
            return
        # 禁止处理增强赋值表达式，如 a+=1、总数-=2 等
        if re.search(r'[\u4e00-\u9fff_a-zA-Z]\w*\s*[\+\-\*/%]=', expr):
            return
        annotation = sep+right
        if not self.contain_operator(expr):
            if expr not in self.variables:
                return


    def calc(self, expr:str)->str:
        pass

    """
    工具类
    """
    def update_variables(self,var_name:str, var_value):
        if var_name in self.constants:
            raise Exception("请勿修改常量")
        self.variables[var_name] = var_value

    def contain_operator(self, expr: str) -> bool:
        return any(op in expr for op in "+-*/%=")

    def is_func_calls(self, expr: str) -> bool:
        metch = self.func_calls_pattern.fullmatch(expr.strip())
