'''
登录类
调用登录接口，获取cookie
'''

import requests


class GetCookie():
    def __init__(self) -> None:
        self.base_url = 'http://shop-xo.hctestedu.com'  # 添加： /index.php?s=/api
        self.public_params = {
            'application': 'web',
            'application_client_type': 'pc'
        }

    def __login(self):
        # 私有函数，这个函数不应该被外部代码直接访问，它主要用于模块内部的逻辑实现。
        # 1.登录
        url = self.base_url + '/index.php?s=/api/user/login'
        request_params = {
            "accounts": "test_777",
            "pwd": "test_777",
            "type": "username"
        }
        all_params = {**self.public_params, **request_params}
        res = requests.post(url=url, json=all_params)
        # res = requests.post(url=url,json=all_params,headers=headers)
        cookie_str = (res.headers[ 'Set-Cookie' ]).split(';')[ 0 ] #'PHPSESSID=70vonjdmboqj3lqd0u6v6oub05'
        cookie_dict = {cookie_str.split('=')[0]:cookie_str.split('=')[1]} # {'PHPSESSID': '70vonjdmboqj3lqd0u6v6oub05'} <class 'dict'>
        return cookie_dict


    def get_cookie(self):
        return self.__login()

# if __name__=='__main__':
#     lc = GetCookie()
    # print(lc.get_cookie())

