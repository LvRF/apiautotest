import pytest
import time
from py._xmlgen import html

'''
改全局配置文件
生成报告时会用到，不用自己手动引用，相当于改了自带库中的配置
'''

import yaml


def pytest_collection_modifyitems(items):
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


# 修改报告名称
def pytest_html_report_title(report):
    #report.title = "接口自动化测试报告"
    with open("./config/config.yaml", "r", encoding='GBK') as f:
        report.title = yaml.load(f, Loader=yaml.FullLoader)["task_line"][0] + "接口自动化测试报告"

# # 使用 pytest_html_report_title 钩子方法
# def pytest_html_report_title(reports):
#     #reports.title = "接口自动化测试报告"
#     with open("./config/config.yaml", "r") as f:
#         reports.config._metadata["Title"] = yaml.load(f, Loader=yaml.FullLoader)["task_line"][0] + "接口测试报告"
#         # reports.title = yaml.load(f, Loader=yaml.FullLoader)["task_line"][0] + "接口测试报告"

# 使用 pytest_configure钩子方法
# def pytest_configure(config):
#     with open("./config/config.yaml", "r") as f:
#         config._metadata["Title"] = yaml.load(f, Loader=yaml.FullLoader)["task_line"][0] + "接口测试报告"

