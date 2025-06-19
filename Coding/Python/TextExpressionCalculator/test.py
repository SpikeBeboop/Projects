varl={
    'abc':12,
    'bcd':3,
}
varl['ca']=1
print('ca' in varl)
print(varl)

varl['ca']=3
print(varl)


expression,sep,right = ''.partition('#')
print(f"expr:{expression}")
print(expression=='')
print(f"right:{sep}{right}")

import re
s="123lkasdf(123)"
pattern = r'^([\u4e00-\u9fa5a-zA-Z_]+)\((.+)\)$'
match = re.fullmatch(pattern, s)
print(match.group(1))