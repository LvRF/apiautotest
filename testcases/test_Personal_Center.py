
import pytest
from utils.login import GetCookie
from utils.my_request import MyRequest
from utils.process_data import ProcessData


class TestPersonal_Center:

    def setup_class(self):
        self.cookie = GetCookie().get_cookie()
        self.request = MyRequest()
        
    def teardown_class(self):
        pass
        
     
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("useraddress_save","Personal_Center"),
    ids=ProcessData.get_ids("useraddress_save","Personal_Center"))
    @ProcessData().decorator_case
    def test_useraddress_save(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/useraddress/save")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"useraddress_save")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("useraddress_index","Personal_Center"),
    ids=ProcessData.get_ids("useraddress_index","Personal_Center"))
    @ProcessData().decorator_case
    def test_useraddress_index(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/useraddress/index")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"useraddress_index")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("useraddress_delete","Personal_Center"),
    ids=ProcessData.get_ids("useraddress_delete","Personal_Center"))
    @ProcessData().decorator_case
    def test_useraddress_delete(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/useraddress/delete")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"useraddress_delete")

    
if __name__=='__main__':
    pass  
