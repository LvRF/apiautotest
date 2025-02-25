# request方法封装

import json
import requests
import traceback
from utils.logger import Logger


class MyRequest:

    def __init__(self):
        pass

    '''
    staticmethod是类的静态方法,放在类里面使用。
    1.在类里边定义方法时，方法不用传self参数；
    2.调用方法：class.fun(x,y)
    
    不同请求方法中，请求头和请求体有部分差异。处理的可能差异如下：
    get:  params
    post: params; headers(格式：json / form-data); files文件传递
    put:  语义是替换。不同于post的是，put需提供对应数据的完整参数。
    '''

    @staticmethod
    def get(url,cookies,case_data,headers):
        # 定义get请求，若请求异常抛出异常报错。url为接口层字段。
        try:
            Logger.info("执行用例: [{}]".format(case_data["case_name"]))
            Logger.info("请求方式: [{}]".format("GET"))
            Logger.info("请求地址: [{}]".format(url))
            Logger.info("请求参数: [{}]".format(case_data["params"]))

            params = case_data['params']
            response = requests.get(url=url, cookies=cookies, params=params)

            return json.loads(response.text)
        except Exception:
            Logger.error("用例[{0}]失败原因[{1}]".format(case_data["case_name"],traceback.format_exc(limit=1)))   # traceback.format_exc(limit=1)：把异常的堆栈信息打印出来形成字符串返回，此处是打印最后一条。
            raise  #raise语句用于抛出异常。当程序运行到raise语句时，它会立即停止当前代码块的执行，并向上层调用者抛出一个指定类型的异常。

    @staticmethod
    def post(url,cookies,case_data,headers):
        # 定义post请求，若请求异常抛出异常报错。url为接口层字段。
        try:
            Logger.info("执行用例: [{}]".format(case_data[ "case_name" ]))
            Logger.info("请求方式: [{}]".format("POST"))
            Logger.info("请求地址: [{}]".format(url))
            Logger.info("请求参数: [{}]".format(case_data[ "data" ]))
            Logger.info("请求参数: [{}]".format(case_data[ "params" ]))

            params = case_data['params']
            data = case_data['data'] # post请求体

            if headers == 'json':
                # print('【debug】headers == "json" 发起请求')
                response = requests.post(url=url, cookies=cookies, json=data, params=params)

            elif headers == 'form-data':
                files = {
                    "files": open(case_data["files"],"rb") if case_data["files"] else None
                }
                response = requests.post(url=url,cookies=cookies,data=data,params=params,files=files)

            else:
                response = requests.post(url=url,cookies=cookies,data=data,params=params)

            return json.loads(response.text)
        except Exception:
            Logger.error("用例[{0}]失败原因 \n [{1}]".format(case_data[ "case_name" ], traceback.format_exc(limit=1)))
            raise  #raise语句用于抛出异常。当程序运行到raise语句时，它会立即停止当前代码块的执行，并向上层调用者抛出一个指定类型的异常。

