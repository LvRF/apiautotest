from string import Template
# 一个模块对应一个py用例脚本文件

BASE_TEMPLATE = Template(
'''
import pytest
from utils.login import GetCookie
from utils.my_request import MyRequest
from utils.process_data import ProcessData


class Test${module_code}:

    def setup_class(self):
        self.cookie = GetCookie().get_cookie()
        self.request = MyRequest()
        
    def teardown_class(self):
        pass
        
    ${case_template}
    
if __name__=='__main__':
    pass  
'''
)



# 入参：interface_code、module_code、url、method、headers
CASE_TEMPLATE = Template(
''' 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("${interface_code}","${module_code}"),
    ids=ProcessData.get_ids("${interface_code}","${module_code}"))
    @ProcessData().decorator_case
    def test_${interface_code}(self,case_data):
        url = ProcessData().replace_url("${url}")
        response = self.request.${method}(url=url,cookies=self.cookie,headers="${headers}",case_data=case_data)
        return (response, case_data,"${interface_code}")
'''
)

