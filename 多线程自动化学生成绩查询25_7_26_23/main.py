# 学生成绩查询自动化脚本
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from openpyxl import Workbook
import threading
import column
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
opt = Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_argument('--window-size=1920,1080')

class Work:
    def __init__(self):  
        self.visited = {}
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = 'cic'
        self.ws.append(['ID', 'Name', 'Score', 'Rank'])
        self.excel_lock = threading.Lock()
        self.error_cnt = 0
        self.right_cnt = 0
        # 加载学生信息列数据
        self.column_ID = column.column_ID
        self.column_Name = column.column_Name
        self.visited = {}
        print(len(self.column_ID))

    def work(self, i):
        try:
            wd = Chrome(options=opt)
            wd.get('https://z9lbopmd.yichafen.com/qz/138Owtgzjt')
            #sleep(1)
            # 等待页面加载完成
            webDriverWait = WebDriverWait(wd, 10)
            webDriverWait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[placeholder="请输入学号"]')))
            # 定位学号和姓名输入框
            element_id = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入学号"]')
            element_name = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入姓名"]')

            # 输入学号和姓名
            element_id.send_keys(self.column_ID[i])
            element_name.send_keys(self.column_Name[i])
            
            # 点击提交按钮
            element_link = wd.find_element(By.ID, 'yiDunSubmitBtn')
            element_link.click()
            # 等待页面加载完成
            target = wd.window_handles[-1]
            wd.switch_to.window(target)
            webDriverWait = WebDriverWait(wd, 10)
            webDriverWait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'right_cell')))
            '''
            for handle in wd.window_handles:
                wd.switch_to.window(handle)
                if '加权' in wd.title:
                    break
            '''
            # 定位包含成绩信息的元素
            element_right = wd.find_elements(By.CLASS_NAME, 'right_cell')
            data = [element.text for element in element_right]
            with self.excel_lock:
                self.ws.append(data)
            right_cnt += 1
            print(f'第{right_cnt}个', data[0])
            
        except Exception as e:
            print('错误：' , e)
            self.error_cnt += 1

        finally:
            if wd:
                wd.quit()


    def run(self):
        threads = []
        for i in range(1, len(self.column_ID)):
            if self.column_ID[i] in self.visited:
                continue
            self.visited[self.column_ID[i]] = True
            t1 = threading.Thread(target=self.work, args=(i,))
            t1.start()
            threads.append(t1)
            sleep(0.9) 
        for t in threads:
            t.join()
        
        self.wb.save('result.xlsx')
        print(f'成功{self.right_cnt}个，失败{self.error_cnt}个')

if __name__ == '__main__':
    worker = Work()
    worker.run()






