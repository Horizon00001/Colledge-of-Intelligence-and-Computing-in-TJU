import sys
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from openpyxl import Workbook
import threading
import column
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from configparser import ConfigParser
from random import uniform


opt = Options()
opt.add_argument('--allow-insecure-localhost') 
opt.add_argument("--incognito")
opt.add_argument('-ignore-certificate-errors')
opt.add_argument('-ignore -ssl-errors')
opt.add_argument('--headless')   
opt.add_argument('--disable-images')     
opt.add_argument('--disable-gpu')
opt.add_argument('--window-size=1920,1080')
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--disable-software-rasterizer')
opt.add_argument('--disable-picture-in-picture')



class Work:
    def __init__(self):  
        self.config = ConfigParser()
        self.config.read("config.ini", encoding="utf-8")
        self.url = self.config['Website']['query_url']
        self.max_tasks = int(self.config["Settings"]["query_max_tasks"])
        self.internal_page = float(self.config["Settings"]["query_interval_time_page"])
        print(f"正在查询: {self.url}")
        print(f"最大进程数为:{self.max_tasks}")
        print(f"网页预留间隔为:{self.internal_page}")
        self.visited = {}
        self.wb = Workbook()
        self.ws = self.wb.active
        self.excel_lock = threading.Lock()
        self.visited_lock = threading.Lock()  
        self.right_cnt_lock = threading.Lock()
        self.error_cnt = 0
        self.right_cnt = 0
        self.column_ID = column.column_ID
        self.column_Name = column.column_Name
        self.visited = {} 

    def work(self, i, wd):
        try:
            with self.visited_lock:
                if i  > len(self.column_ID) - 1:
                    return
                if self.column_ID[i] in self.visited:
                    return
                self.visited[self.column_ID[i]] = True

            wd.get(self.url)
            # 等待页面加载完成
            webDriverWait = WebDriverWait(wd, self.internal_page)
            webDriverWait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="请输入学号"]')))
            # 定位学号和姓名输入框
            element_id = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入学号"]')
            element_name = wd.find_element(By.CSS_SELECTOR, '[placeholder="请输入姓名"]')

            # 输入学号和姓名
            element_id.send_keys(self.column_ID[i])
            element_name.send_keys(self.column_Name[i])
            # 点击提交按钮
            def click1():
                element_link = wd.find_element(By.CSS_SELECTOR, '.kd-button.kd-button-primary.kd-button-xl')
                element_link.click()

                target = wd.window_handles[-1]
                wd.switch_to.window(target)
                
                webDriverWait = WebDriverWait(wd, self.internal_page)
                webDriverWait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='src-pc-components-requery-index-module__requery-tips']")))
                if "查询结果为空" in wd.page_source:
                    wd.quit()
                    print(f"{self.column_Name[i]} 学生不存在，结束进程")
                    sys.exit(0)
                
                webDriverWait = WebDriverWait(wd, self.internal_page)
                webDriverWait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='src-pc-components-result-field-value-index-module__value']")))
                print("正在获取...")
                list = wd.find_elements(By.CSS_SELECTOR, "[class='src-pc-components-result-field-value-index-module__value']")
                data = [li.text for li in list]
                with self.excel_lock:
                    self.ws.append(data)
                with self.right_cnt_lock:
                    self.right_cnt += 1
                print(f"一共 {len(self.column_ID)} 个，第 {self.right_cnt} 个已获取", data)
                
                

            def click2():#'Work' object has no attribute 'right
                element_link = wd.find_element(By.ID, 'yiDunSubmitBtn')
                element_link.click()
                # 等待页面加载完成
                target = wd.window_handles[-1]
                wd.switch_to.window(target)
                webDriverWait = WebDriverWait(wd, self.internal_page)
                webDriverWait.until(EC.presence_of_element_located((By.CLASS_NAME, 'right_cell')))
                print("正在获取...")
                element_right = wd.find_elements(By.CLASS_NAME, 'right_cell')
                data = [element.text for element in element_right]
                with self.excel_lock:
                    self.ws.append(data)
                with self.right_cnt_lock:
                    self.right_cnt += 1
                print(f"一共 {len(self.column_ID)} 个，第 {self.right_cnt} 个已获取", data)

            if "yichafen" in self.url:
                click2()
            elif "web.wps.cn" in self.url:
                click1()
            wd.delete_all_cookies()
            
        except Exception as e:
            if wd:
                print("重新加载网页", e)
                wd.delete_all_cookies()
                self.work(i, wd)
            else:
                print("重新打开浏览器")
                wd = Chrome(options=opt)
                sleep(uniform(1,2))
                print(e)
                print('正在重新开始查询：', self.column_ID[i], self.column_Name[i])
                self.work(i, wd)
        finally:
            pass
            

    
    def run1(self):
        wd = Chrome(options=opt)
        for i in (range(1, len(self.column_ID))):
            self.work(i, wd)
        wd.quit()
    '''
    def run2(self):
        wd = Chrome(options=opt)
        for i in (range(len(self.column_ID))):
            self.work(len(self.column_ID) - i - 1, wd)
        wd.quit()
    def run3(self):
        wd = Chrome(options=opt)
        for i in (range(len(self.column_ID))):
            self.work(len(self.column_ID) // 3 + i, wd)
        wd.quit()
    def run4(self):
        wd = Chrome(options=opt)
        for i in (range(len(self.column_ID))):
            self.work(len(self.column_ID) // 3  + i, wd)
        wd.quit()
    '''

    def thread(self):
        threads = []
        total_tasks = len(self.column_ID)
        pbar = tqdm(total=total_tasks, desc="总进度", unit="次数")
        for _ in range(self.max_tasks):
            t = threading.Thread(target=self.run1)
            t.start()
            sleep(0.1)
            threads.append(t)
        
        
        while any(t.is_alive() for t in threads):
            with self.right_cnt_lock:
                pbar.n = self.right_cnt 
                pbar.refresh()
            sleep(0.1) 
        pbar.close()
        for t in threads:
            t.join()

        self.wb.save('result.xlsx')
        print(f'成功{self.right_cnt}个，失败{len(self.column_ID) - 1 - self.right_cnt}个')
        for i in range(1, len(self.column_ID)):
            if self.visited[self.column_ID[i]]:
                continue
            print(f'失败 (学号: {self.column_ID[i]}, 姓名: {self.column_Name[i]})')


if __name__ == '__main__':
    worker = Work()
    worker.thread()
