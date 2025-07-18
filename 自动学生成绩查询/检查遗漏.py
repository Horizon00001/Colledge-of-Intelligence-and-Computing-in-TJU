#由于潜在网络问题未能获取，这里写了一个py文件便于检查人数，遗漏的人数写在ans中
#ans跑出来绝大多数的学号无法查询（笔者推测已进入拔尖班学习）
s = ""
with open('成绩.txt', 'r', encoding='utf-8') as of:
    for line in of:
        s += line
l = []
ans = []
with open('D:\VSCodeFile\Python\学号.txt', 'r', encoding='utf-8') as f:
    for line in f:
        l = line.split()
        if '3024244' in l[0]:
            if l[0] not in s:
                ans.append(l[0])
print(ans)
print(len(ans))