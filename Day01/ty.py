import re
#目标字符串
s = 'Alex:1994,Sunny:1996'
pattern = r'\w+:\d+'  #正则表达式
# l = re.findall(pattern,s)
# print(l)
regex = re.compile(pattern)
l = regex.findall(s,0,12)
print(l)

s = re.sub()



