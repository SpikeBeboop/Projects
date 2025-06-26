import math

class Calc:
    def __init__(self):
        self.context = {
            "__builtins__": None,
            "sin": math.sin,
            "cos": math.cos,
            "sqrt": math.sqrt,
            "log": math.log,
            "pi": math.pi,
            "e": math.e,
        }

    def __call__(self, content:str):
        return self.calculate(content)

    def string_processing(self, content, position):
        pass

    def calculate(self, expr:str):
        try:
            result = eval(expr, self.context)
            return result
        except Exception:
            return "表达式错误"