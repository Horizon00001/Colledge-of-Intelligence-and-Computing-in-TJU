# 学生信息查询系统

## 项目简介
本项目实现了一个基于Selenium的多线程学生信息查询工具，能够自动从指定网站批量查询学生信息，并将结果保存到Excel文件中。

## 文件说明

### 1. main.py
主程序文件，包含核心查询逻辑：
- 使用Selenium自动化浏览器操作
- 多线程并发查询提高效率（默认10线程）
- 支持无头模式(headless)运行
- 自动保存查询结果到result.xlsx
- 提供进度条显示查询进度

### 2. cic.xlsx
学生数据源文件，包含两列数据：
- A列：学号
- B列：姓名

### 3. column.py
数据加载模块，负责：
- 从cic.xlsx读取学生数据
- 将学号和姓名分别存储在column_ID和column_Name列表中

## 使用说明

1. **环境准备**：
   - 安装Python 
   - 安装依赖库：pip install selenium openpyxl tqdm configparser

2. **配置修改**：
- 如需修改查询URL，编辑main.py中Work类的url属性。
- 修改线程数：调整max_tasks值

3. **运行程序**：
-main.py


4. **结果查看**：
- 查询结果将保存在result.xlsx中
- 控制台会显示查询进度和统计信息

## 注意事项

1. 请确保cic.xlsx与程序在同一目录
2. 查询网站可能需要验证码或动态加载，程序可能需要相应调整
3. 默认使用无头模式，如需调试可移除--headless参数

## 作者
-by zhl
-QQ：1302485828


## 成绩分布

<img width="3569" height="2108" alt="score_distribution" src="https://github.com/user-attachments/assets/cde1ebc1-ff7e-4a45-bb45-b98c7dd4ea74" />

## 效果

<img width="1952" height="455" alt="屏幕截图 2025-08-09 172049" src="https://github.com/user-attachments/assets/1dc9b3ae-0f6a-4623-a031-a09abde42c88" />




