import pytest,os
from utils.analyseExcel_utils import AnalyseExcel
from utils.process_data import ProcessData
from utils.generate_script import GenerateScript
from datetime import datetime


excel_file = './data/TestCase01.xlsx'
now = datetime.now().strftime('%Y%m%d%H%M%S') #20241221000139
# now = time.strftime('%Y-%m-%d %H_%M_%S') #2024-12-21 00_02_07


if __name__=='__main__':
    # pytest.main(['-vs','./testcases/case_debuging.py'])

    ae = AnalyseExcel(excel_file)
    execl_data = ae.read_module_data()

    pd = ProcessData()
    # 此处second_data用save_to_json()返回没处理过的execl_data。是为了保证用例脚本中的数据来源case_data.json、second_data数据一致性。避免影响测试结果的准确性。
    second_data = pd.save_to_json(execl_data) #此处，second_data是execl_data的副本。它们值相同，但在内存中是不同的对象。

    gs = GenerateScript()
    script = gs.generate_script(second_data)


    # pytest.main(
    #     [
    #         '-v',
    #         '--tb=native',
    #         './testcases/test_Goods_Mgmt.py',
    #         './testcases/test_Personal_Center.py',
    #         '--html=./reports/reports-{}.html'.format(now),
    #         '--self-contained-html'
    #         # '--junitxml=./reports/reports.xml',
    #         ]
    #     )


    # # allure 报告 (直接打开html报告会显示loading，可通过终端工具执行命令： allure open/serve reports，会直接打开html报告 )
    pytest.main(['-sq','./testcases/test_Personal_Center.py','--alluredir=./result'])
    os.system(f'allure generate ./result -o ./reports --clean')





