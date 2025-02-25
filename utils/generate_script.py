from config.template import BASE_TEMPLATE,CASE_TEMPLATE
from utils.load import LoadYaml
from utils.logger import Logger
from string import Template


class GenerateScript:


    def __init__(self):
        self.base_template = BASE_TEMPLATE
        self.case_template = CASE_TEMPLATE
        # 【补充】config.yaml中写默认路径(指定到文件夹)
        self.script_path = LoadYaml().read()['script_path'] #LoadYaml后面需带()，否则会报错：TypeError: read() missing 1 required positional argument: 'self'
        self.report_path = LoadYaml().read()['report_path']

    def create_case_fuc(self,module_code,interface_lists)->str:
        # 思路：本函数生成的脚本中，一个用例函数对应一个接口，其中包含多个用例。所以本函数的入参应是 接口层级 的 interface_lists
        #  本函数生成的用例脚本，有多个。是通过遍历一个模块中的接口列表，一个接口对应生成一个 函数脚本。故此处需要用：case_temp = case_temp +「具体生成步骤」实现用例脚本的生成。
        case_temp = ''
        for interface_dict in interface_lists:
            Logger.info("添加接口{}用例".format(interface_dict[ "interface_code" ]))
            case_temp = case_temp + self.case_template.substitute(
                interface_code = interface_dict['interface_code'],
                module_code = module_code,
                url = interface_dict['url'],
                method = interface_dict['method'],
                headers = interface_dict['headers']
            )
        return case_temp

    def create_case_class(self,module_dict)->Template:
        # 思路：本函数是针对一个模块的 测试用例类 函数，所以入参是 模块层级的 module_dict
        return self.base_template.substitute(
            module_code = module_dict['module_code'],
            case_template = self.create_case_fuc(
                interface_lists = module_dict['interface_list'],
                module_code = module_dict['module_code'])
        )

    def generate_script(self,module_list)->None:
        Logger.info("================生成用例脚本====================")
        for module_dict in module_list:
            Logger.info("生成测试类{}".format(module_dict["module_code"]))
            if module_dict["situation_code"]:
                file_path = self.script_path + "test_" + str(module_dict["situation_code"]) + ".py"
            else:
                file_path = self.script_path + "test_" + str(module_dict["module_code"]) + ".py"
            with open(file_path,'w',encoding='utf-8',errors='ignore') as f: #当设置为 'ignore' 时，如果在读写文件过程中遇到了无法按照指定的 utf-8 编码进行处理的字符（例如一些非法的字节序列），Python 会直接忽略这些错误，继续处理其他正常的字符。
                f.write(self.create_case_class(module_dict))