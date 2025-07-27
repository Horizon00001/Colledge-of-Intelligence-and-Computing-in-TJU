# 学生成绩查询自动化工具

这是一个基于Python的多线程学生成绩查询自动化脚本，能够批量查询学生成绩并导出结果。

## 功能特点

- 多线程并发查询，提高查询效率
- 自动将查询结果导出到Excel文件
- 详细的错误处理和结果统计

## 环境要求

- Python 3.8+
- Chrome浏览器
- ChromeDriver (需与Chrome版本匹配)

## 安装步骤

1. 克隆或下载本项目到本地
2. 安装依赖包：
   ```
   pip install openpyxl selenium tqdm 
   ```

## 使用方法

1. 确保column.py文件中包含正确的学号和姓名数据
2. 运行查询脚本：
   ```
   python main.py
   ```
3. 查询结果将自动保存到result.xlsx文件

## 成绩分布

<img width="3569" height="2108" alt="score_distribution" src="https://github.com/user-attachments/assets/cde1ebc1-ff7e-4a45-bb45-b98c7dd4ea74" />


## 文件说明

- main.py: 核心查询逻辑实现，包含多线程管理和Excel导出
- column.py: 存储学生学号和姓名数据
- cic.xlsx: 学生信息Excel文件
- result.xlsx: 查询结果输出文件

## 注意事项

- 请确保ChromeDriver已添加到系统PATH或与脚本同目录
- 查询速度受网络状况和服务器响应影响
- 程序会自动统计成功和失败的查询数量
- 失败的查询会在控制台显示具体学号和姓名

## 故障排除

- 如遇ChromeDriver相关错误，请检查Chrome浏览器和Driver版本是否匹配
- 如遇网络问题，可尝试调整main.py中的线程休眠时间
- 若出现验证码或访问限制，请稍后再试
