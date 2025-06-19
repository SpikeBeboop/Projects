import math
from PySide6.QtCore import QObject, Signal

class Calc:
    def __init__(self, label:QLabel):
        self.context = {
            "__builtins__": None,
            "sin": math.sin,
            "cos": math.cos,
            "sqrt": math.sqrt,
            "log": math.log,
            "pi": math.pi,
            "e": math.e,
        }

    """
    计算主入口
    """
    def calc(self, context:str):
        pass
