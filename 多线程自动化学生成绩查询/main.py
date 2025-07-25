# 学生成绩查询自动化脚本
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from openpyxl import Workbook
import threading
import column
'''
opt = Options()
#opt.add_argument('--headless')
#opt.add_argument('--disable-gpu')
'''

class Work:
    def __init__(self):  
        self.visited = {}
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = 'cic'
        self.ws.append(['ID', 'Name', 'Score', 'Rank'])
        self.excel_lock = threading.Lock()
        self.error_cnt = 0

    def work(self, i):
        try:
            wd = Chrome()
            wd.get('https://z9lbopmd.yichafen.com/qz/138Owtgzjt')
            sleep(1)
            # 定位学号和姓名输入框
            element_id = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入学号"]')
            element_name = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入姓名"]')

            # 输入学号和姓名
            element_id.send_keys(column.column_ID[i])
            element_name.send_keys(column.column_Name[i])
            
            # 点击提交按钮
            element_link = wd.find_element(By.ID, 'yiDunSubmitBtn')
            element_link.click()
            sleep(1)

            # 切换到包含"加权"关键词的窗口
            for handle in wd.window_handles:
                wd.switch_to.window(handle)
                if '加权' in wd.title:
                    break

            # 定位包含成绩信息的元素
            element_right = wd.find_elements(By.CLASS_NAME, 'right_cell')
            data = [element.text for element in element_right]
            with self.excel_lock:
                self.ws.append(data)
                print(data[0])
            wd.quit()
        except:
            print('错误')
            self.error_cnt += 1


    def run(self):
        threads = []
        for i in range(1, len(column.column_ID)):
            t1 = threading.Thread(target=self.work, args=(i,))
            t1.start()
            threads.append(t1)
            sleep(0.9) 
        for t in threads:
            t.join()
        

        self.wb.save('result.xlsx')





if __name__ == '__main__':
    worker = Work()
    worker.run()





