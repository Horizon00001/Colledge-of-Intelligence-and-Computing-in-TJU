#由于潜在网络问题未能获取，这里写了一个py文件便于检查人数，遗漏的人数写在ans中
#ans跑出来绝大多数的学号无法查询（笔者推测已进入拔尖班学习）
#如果网站查询错误过多会要求输入验证码
#拔尖班剔除

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

bajianban = """3024001053
3024232129
3024001096
3024244524
3024234634
3024244408
3024244569
3024244529
3024001416
3024244288
3024244039
3024244522
3024001557
3024244508
3024209110
3024244364
3024210033
3024233099
3024206098
3024244130
3024244069
3024209079
3024244442
3024202404
3024244411
3024244134
3024244229
3024001017
3024232076

3024244323
3024244330
3024244200
3024244304
3024244085
3024244005
3024244512
3024244245
3024244473
3024244383
3024244001
"""


s = ""
with open('.\自动学生成绩查询\成绩.txt', 'r', encoding='utf-8') as of:
    for line in of:
        s += line

l = []
ans = []
mydict2 = {}
with open('.\自动学生成绩查询\学号.txt', 'r', encoding='utf-8') as f:
    for line in f:
        l = line.split()
        if '3024244' in l[0]:
            if l[0] in bajianban:
                continue
            if l[0] not in s:
                mydict2[l[0]] = l[1]
                ans.append(l[0])

with open('.\自动学生成绩查询\学号转专业.txt', 'r', encoding='utf-8') as f:
    for line in f:
        l = line.split()
        if l[0] not in s:
            mydict2[l[0]] = l[1]
            ans.append(l[0])
print(len(ans))
print(mydict2)


"""
for i in ans:
    # 初始化Chrome浏览器驱动
    wd = webdriver.Chrome()

    # 打开成绩查询网站
    wd.get('https://z9lbopmd.yichafen.com/qz/138Owtgzjt')

    # 定位学号和姓名输入框
    element_id = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入学号"]')
    element_name = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入姓名"]')

    # 输入学号和姓名
    element_id.send_keys(i)
    element_name.send_keys(mydict2[i])
    
    #输入验证码
    time.sleep(7)

    # 点击提交按钮
    element_link = wd.find_element(By.ID, 'yiDunSubmitBtn')
    element_link.click()
    
    # 等待2秒让页面加载
    time.sleep(2)
    
    # 切换到包含"加权"关键词的窗口
    for handle in wd.window_handles:
            wd.switch_to.window(handle)
            if '加权' in wd.title:
                break

    # 定位包含成绩信息的元素
    element_right = wd.find_elements(By.CLASS_NAME, 'right_cell')

    # 将成绩信息写入文件
    with open('.\自动学生成绩查询\成绩.txt', 'a', encoding='utf-8') as f:
            for i in range(len(element_right)):
                f.write(element_right[i].text + '  ')  # 写入每个成绩项
            f.write('\n')  # 换行
    
    # 关闭浏览器
    wd.quit()
"""
