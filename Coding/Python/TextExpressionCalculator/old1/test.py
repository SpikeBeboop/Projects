import math

context = {
    "__builtins__": None,  # 禁用所有内建函数
    "sin": math.sin,
    "cos": math.cos,
    "sqrt": math.sqrt,
    "log": math.log,
    "pi": math.pi,
    "e": math.e
}

expr = 'a=2'
exec(expr, context)
print(context)

print(eval('# test\nsin(pi)', context))