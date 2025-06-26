# from idlelib.run import show_socket_error
# from logging import raiseExceptions
#
# from asteval import Interpreter
#
# # 创建解释器实例
# aeval = Interpreter(raise_errors=True)
#
# # 定义一些变量供表达式使用
# aeval.symtable['x'] = 5
# aeval.symtable['y'] = 0
#
# # 要计算的表达式
# expression = "1+2-"
#
# try:
#     # 执行表达式计算
#     aeval.error = []
#     result = aeval(expression,raise_errors=True)
#     print(f"计算结果: {result}")
# except SyntaxError as e:
#     print(f"语法错误: {e}")
# except NameError as e:
#     print(f"名称错误: {e}")
# except TypeError as e:
#     print(f"类型错误: {e}")
# except ZeroDivisionError:
#     print("错误: 除数不能为零")
# except Exception as e:
#     print(f"其他错误: {e}")
# finally:
#     # 无论是否发生异常，都会执行的清理代码
#     print("表达式计算完成")

# from calc111 import Calculator
# import util.tool
# calc = Calculator()
#
# expr = "(1/2)+1=21+3=46-1"
# calc.calculate(expr)
# # import  util.tool
# # from util.tool import replace_first_number
# #
# # exp = ""
# # replace_first_number(exp,"11")
# # print(replace_first_number(exp,"11"))

a=12
b=a
print(b)
a=11
print(b)