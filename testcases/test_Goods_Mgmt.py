
import pytest
from utils.login import GetCookie
from utils.my_request import MyRequest
from utils.process_data import ProcessData


class TestGoods_Mgmt:

    def setup_class(self):
        self.cookie = GetCookie().get_cookie()
        self.request = MyRequest()
        
    def teardown_class(self):
        pass
        
     
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("init_search","Goods_Mgmt"),
    ids=ProcessData.get_ids("init_search","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_init_search(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/search/index")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"init_search")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("goods_detail","Goods_Mgmt"),
    ids=ProcessData.get_ids("goods_detail","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_goods_detail(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/goods/detail")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"goods_detail")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("usergoodsbrowse_index","Goods_Mgmt"),
    ids=ProcessData.get_ids("usergoodsbrowse_index","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_usergoodsbrowse_index(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/usergoodsbrowse/index")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"usergoodsbrowse_index")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("usergoodsbrowse_delete","Goods_Mgmt"),
    ids=ProcessData.get_ids("usergoodsbrowse_delete","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_usergoodsbrowse_delete(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/usergoodsbrowse/delete")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"usergoodsbrowse_delete")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("goods_favor","Goods_Mgmt"),
    ids=ProcessData.get_ids("goods_favor","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_goods_favor(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/goods/favor")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"goods_favor")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("usergoodsfavor_index","Goods_Mgmt"),
    ids=ProcessData.get_ids("usergoodsfavor_index","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_usergoodsfavor_index(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/usergoodsfavor/index")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"usergoodsfavor_index")
 
    @pytest.mark.parametrize("case_data",ProcessData.get_case_lists("usergoodsfavor_cancel","Goods_Mgmt"),
    ids=ProcessData.get_ids("usergoodsfavor_cancel","Goods_Mgmt"))
    @ProcessData().decorator_case
    def test_usergoodsfavor_cancel(self,case_data):
        url = ProcessData().replace_url("${url.lingplatform}/usergoodsfavor/cancel")
        response = self.request.post(url=url,cookies=self.cookie,headers="json",case_data=case_data)
        return (response, case_data,"usergoodsfavor_cancel")

    
if __name__=='__main__':
    pass  
