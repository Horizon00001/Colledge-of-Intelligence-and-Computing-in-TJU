# 学生成绩查询自动化脚本

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 初始化字典用于存储学号和姓名
mydict = {}

# 读取第一个文件"学号.txt"，提取学号和姓名
with open('.\自动学生成绩查询\学号.txt', 'r', encoding='utf-8') as ifile:
    for line in ifile:
        l = line.split()  # 按空格分割每行
        if '3024244' not in l[0]:  # 筛选特定学号段
            continue
        mydict[l[0]] = l[1]  # 将学号作为key，姓名作为value存入字典
        #print(mydict[l[0]])

# 读取第二个文件"学号转专业.txt"，补充或更新学号和姓名
with open('.\自动学生成绩查询\学号转专业.txt', 'r', encoding='utf-8') as ifile2:
    for line in ifile2:
        l = line.split()  # 按空格分割每行
        mydict[l[0]] = l[1]  # 更新字典中的学号姓名对应关系
        #print(mydict[l[0]])

# 创建或打开"成绩.txt"文件，写入表头
with open('.\自动学生成绩查询\成绩.txt', 'a', encoding='utf-8') as f:
    f.write('学号  姓名  加权  排名' + '\n')  # 写入

# 遍历字典中的每个学号
for i in mydict.keys():
    # 初始化Chrome浏览器驱动
    wd = webdriver.Chrome()

    # 打开成绩查询网站
    wd.get('https://z9lbopmd.yichafen.com/qz/138Owtgzjt')

    # 定位学号和姓名输入框
    element_id = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入学号"]')
    element_name = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入姓名"]')

    # 输入学号和姓名
    element_id.send_keys(i)
    element_name.send_keys(mydict[i])
    
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
