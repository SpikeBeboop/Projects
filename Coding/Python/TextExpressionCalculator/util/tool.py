import re

def is_number(s):
    return re.fullmatch(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', s) is not None

def replace_first_number(expr: str, new_number: str) -> str:
    if expr=="":
        return new_number
    return re.sub(r'\d+', new_number, expr, count=1)