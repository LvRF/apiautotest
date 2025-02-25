'''
工具包：数据处理封装函数
【语法】
if not yaml_dict.get('task_line',0): #检查字典yaml_dict中键'task_line'的值是否为假值，如果该键不存在或者值为假值，则条件判断结果为True，否则为False。

1. @staticmethod函数装饰器：用于定义静态方法。静态方法是属于类而不是类的实例的方法。
    不依赖于类的实例或者类本身的状态（如实例属性或类属性），它更像是一个工具方法，只是逻辑上被放在了类的内部，用于提高代码的组织性和可读性。
    调用： class().method()
2. continue：控制流语句，用于for/while循环结构。当在循环体内遇到continue语句时，它会立即终止当前迭代的剩余部分，并跳转到循环的下一次迭代。
3. str.strip(): 去除字符串前后的空格
4. 在 Python 中，以下这些情况会被视为 “假值”：False、None、0（整数零）、0.0（浮点数零）、空字符串 ""、空列表 []、空字典 {}、空元组 () 等。
    在 Python 中，以下这些情况会被视为 “真值”：非空的字符串、非空的列表、非空的字典、非空的元组、非零的数值（整数、浮点数等）以及 True 本身等。
5. if判断条件是否为‘假’，只需在条件前加 not。---【if 条件1 or 条件2：】 任意一部分为 True，整个条件判断的结果就为 True，对应的 if 语句块内的代码将会被执行。
    例如：if not yaml_dict or not yaml_dict.get(interface_code):
    1）这里检查变量 yaml_dict 是否为 “假值”。所以当 yaml_dict 是「4」 “假值” 类型中的任何一种时，not yaml_dict 这个表达式就会返回 True，也就意味着满足整个 if 语句的条件判断。
    2）not 运算符对 yaml_dict.get(interface_code) 的返回结果取反，所以当 yaml_dict.get(interface_code) 返回的值是 “假值”（例如 None，
       也就是对应的键在字典中不存在或者对应的值本身就是 “假值” 类型）时，not yaml_dict.get(interface_code) 这部分的表达式就返回 True，同样也会使得整个 if 语句的条件判断为 True。
6. 【实践结果】 类 里面的函数中，如果需要引用到本类，要么用self代替，要么用 本类型() 代替。
7. "assert {} == {}".format(a,b)  等价于  assert {a} == {b}".format(a=a,b=b) 【注意】{}中有变量名时，format()中需对变量名进行赋值，否则会报错。
8. 在 Python 中，raise 语句用于抛出一个异常。当程序执行到 raise 语句时，会立即停止当前代码块的执行，并将异常向上传递，直到被适当的异常处理机制（如 try - except 块）捕获，或者导致程序终止并显示错误信息。
'''

import json
import re

import jsonpath
import yaml
from utils.analyseExcel_utils import AnalyseExcel
from utils.load import LoadYaml,LoadJson
from utils.logger import Logger
from utils.assertion import Assertion

class ProcessData:


    def __init__(self):
        self._ly = LoadYaml()
        self._lj = LoadJson()

    # def get_module_list(self):
    #     # 【debug】获取excel数据 -> list
    #     excel_file = '../data/TestCase01.xlsx'
    #     ae = AnalyseExcel(excel_file)
    #     execl_data = ae.read_module_data()
    #     return execl_data

    def save_to_json(self, module_list) -> list:
        # 1. 将Excel数据(module_list) 存储到 './data/case_data.json', 同时返回入参module_list
        with open('./data/case_data.json', 'w') as f:
            Logger.info("用例数据写入json")
            f.write(json.dumps(module_list,ensure_ascii=False))  # 另一种写法(不适合用于复杂情况，否则代码可读性差)： json.dump(excel_data,f)
        # 2. 将业务线、模块、测试场景信息写入到配置文件(./config/field.yaml)
        Logger.info("基本信息写入配置文件")
        for module_dict in module_list:
            self.write_module_info(module_dict['task_line'],module_dict['module_name'],module_dict['situation_name'])
        return module_list

    def write_module_info(self,task_line, module_name, situation_name):
        # 将业务线、模块、测试场景 信息写入到配置文件(./config/field.yaml)
        yaml_dict = self._ly.read()

        if not yaml_dict.get('task_line',0): #检查字典yaml_dict中键'task_line'的值是否为假值，如果该键不存在或者值为假值，则条件判断结果为True，否则为False。
            yaml_dict['task_line'] = [task_line]
        else:
            yaml_dict['task_line'].append(task_line) #【25/2/16 问题】这样处理，会每次执行都追加写入一遍

        if not yaml_dict.get('module_name',0):
            yaml_dict['module_name'] = [module_name]
        else:
            yaml_dict['module_name'].append(module_name)

        if not yaml_dict.get('situation_name',0):
            yaml_dict['situation_name'] = [situation_name]
        else:
            yaml_dict['situation_name'].append(situation_name)

        self._ly.update(yaml_dict) #把更新后的字典写入yaml文件

    '''
    【待封装函数】
    get_case_lists(self,interface_code,module_code) -->根据excel_data 的module_code+interface_code,从json文件中获取对应用例数据 casedata
    get_ids(interface_code,module_code) --> 根据excel_data 的module_code+interface_code,从json文件中获取对应用例数据(用例名称、人员等相关打印信息)
    decorator_case() --> 装饰器函数，请求前参数格式化，请求后相关参数回填。
    replace_url() --> 请求前替换url
    write_to_yaml() --> 写入yaml文件
    update_output_field() --> 接口请求后，更新yaml文件中引用变量的值
    '''

    @staticmethod
    def get_case_lists(interface_code,module_code)->list:
        # 功能：根据excel_data 的module_code+interface_code,从json文件中获取对应用例数据 case_lists
        module_list = ProcessData()._lj.read() # 获取"./data/case_data.json"文件中的数据。格式：read()已转换为python对象(列表中嵌套字典)
        for module in module_list:
            if module['module_code'].strip() == module_code:
                for interface in module['interface_list']:
                    if interface['interface_code'] == interface_code:
                        return interface['case_lists'] #此处返回的case_lists是 已转python对象(列表中嵌套字典)的json数据
                    else:
                        continue #执行此语句 会立即终止当前迭代的剩余部分，并跳转到循环的下一次迭代。
            else:
                continue

    @staticmethod
    def get_ids(interface_code, module_code):
        # 功能：根据excel_data的module_code + interface_code, 从json文件中获取对应用例的部分字段(用例名称、人员等相关打印信息)

        # 24/12/10 比如有两个用例时返回的列表格式：['usergoodsfavor_cancel;post;商品收藏取消操作;lvmc;陈炎清;NO_001;商品收藏取消操作', 'usergoodsfavor_cancel;post;商品收藏取消操作;lvmc;陈炎清;NO_002;debug_商品收藏取消操作']
        # 返回列表内容： interface_code,interface_method,interface_name,tester,developer,case_dict["case_number"],case_dict["case_name"]
        Ids = [ ]
        module_list = ProcessData()._lj.read()
        for module in module_list:
            if module[ 'module_code' ].strip() == module_code:
                for interface_dict in module[ 'interface_list' ]:
                    if interface_dict[ 'interface_code' ] == interface_code:
                        interface_method = interface_dict.get('method', '') #键存在时，返回对应值；键不存在则返回空''
                        interface_name = interface_dict.get('interface_name', '')
                        tester = interface_dict.get('tester', '')
                        developer = interface_dict.get('developer', '')
                        case_lists = interface_dict.get('case_lists', '')

                        for case_dict in case_lists:  # 因为上面的字段都是接口层级的字典，对应一个用例列表，包含多个用例。所以用例字典在这个层级添加。
                            Ids.append(
                                interface_code + ';' +
                                interface_method + ';' +
                                interface_name + ';' +
                                tester + ';' +
                                developer + ';' +
                                case_dict[ 'case_number' ] + ';' +
                                case_dict[ 'case_name' ]
                            )
        return Ids

# 【2/17继续：】
    def write_to_yaml(self,*args):
        '''
        写入yaml配置文件
        【12/13待定格式】 ：
        useraddress_index:
          NO_001:
            id:
            - '17697'
        思路：逐步判断 接口编号、用例编号、引用字段 是否已经存在，再对应更新yaml文件。
        被调用时入参：(self._ly.read(),interface_code,case_number,output_field,field_value)
        '''
        yaml_dict,interface_code,case_number,output_field,field_value = args
        if not yaml_dict or not yaml_dict.get(interface_code):
            field_structure = {
                interface_code: {
                    case_number: {
                        output_field: field_value
                    }
                }
            }
            self._ly.write(field_structure)
        else:
            # 此else中，说明 yaml_dict 中已经存在 interface_code; 以下有 case_number存在/不存在两种情况。
            if yaml_dict[interface_code].get(case_number): # case_number 已存在
                if yaml_dict[interface_code][case_number].get(output_field):
                    yaml_dict[interface_code][case_number][output_field] = field_value
                else:
                    yaml_dict[interface_code][case_number].update({output_field: field_value})
            else: # case_number 不存在
                yaml_dict[interface_code].update(
                    {case_number: {output_field: field_value}}
                )
            self._ly.update(yaml_dict)

    def update_output_field(self,response,interface_code,case_number,output_field)->None:
        '''
        更新 "./config/config.yaml" 文件中 引用变量的值。
        思路：用例中若有 output_field 字段，将接口响应中对应字段值回填到 ’config.yaml‘ 文件中。
        '''
        if output_field:
            for field in output_field.split(';'): #文本用例中，多个引用字段用';'隔开。
                target = field.split('.')[-1] # target可能格式：'id' 或 'id[0]'
                try:
                    match = re.search(r'([^[]+)\[([^\]]+)\]', target) #判断target中是否含有'[]'字符
                    if match:
                        target = match.group(1) # 获取变量名，比如：id
                        content_in_brackets = match.group(2) # 获取 下标
                        # print("提取变量:", left_part)
                        # print("目标列表下标:", content_in_brackets)
                        field_value = jsonpath.jsonpath(response, '$..{}'.format(target))[int(content_in_brackets)]
                    else:
                        field_value = jsonpath.jsonpath(response,'$..{}'.format(target))
                except AttributeError:
                    Logger.error("依赖字段提取失败，返回内容异常：{}".format(response))
                    raise
            Logger.info("依赖字段开始回写,格式为 目标字段:字段值：{}:{}".format(target, field_value))
            self.write_to_yaml(self._ly.read(),interface_code,case_number,target,field_value)
            # Logger.info("回写后的yaml内容：{}".format(self._ly.read()))

    def decorator_case(self,func):
        '''
        功能：请求前入参处理；请求后响应数据回填。 此处入参func为模板中，进行接口请求的函数(即测试用例函数)
        1、模板-请求前入参：interface_code、module_code、url、method、headers
            ---1)入参值处理：其中url值中含有变量，需要替换后才能用于请求。 2)、入参值格式处理：可能需要处理格式的字段有data/params-->封装处理 adapt_case_data()
        2、模板-请求后，通过将响应字段回填-->封装处理 update_output_field()
        '''
        pd = ProcessData()
        def wrapper(self,case_data): # args 同func()入参。此处入参case_data是字典格式。
            # print("【debug】wrapper()函数中的入参 case_data 的类型、数据值: {}, {}".format(type(case_data),case_data))
            pd.adapt_case_data(case_data) # 格式化用例数据(data、params)为标准dict数据
            result = func(self,case_data)
            response,case_data,interface_code = result
            pd.update_output_field(response, interface_code, case_data['case_number'], case_data['output_field'])
            Assertion.resultAssert(response, case_data['assertion'])
        return wrapper

    def adapt_case_data(self,case_data):
        # 格式化用例数据(data、params)为标准dict数据。此处入参 case_data 是字典格式。
        '''
        【思路 24/12/15】
        1、首先知道case_data用例数据中，data为带 $ 符号的字符串、params为null。
        2、「问题1」：直接使用 eval(str) 去尝试转换字符串为字典会 「语法错误」，因为 eval 函数会按照 Python 的语法规则去解析字符串内容，而字符串里的 $ 并不是 Python 语法中合法的字典键值对里的部分。
            「解决方案」：此处 $ 用于传参，故可将变量替换成对应值，再格式化处理。
        3、「问题2」：用例数据中含有 null 会报错。--因为Python 中没有名为 Null 的类型，与之类似的是 None。--故需将其进行替换。
        '''
        Logger.info("格式化case_data {}".format(case_data))
        case_data['data'] = self.str2_dict(self.replace_case_data(case_data['data']))
        case_data['params'] = self.str2_dict(self.replace_case_data(case_data['params']))

    def str2_dict(self,str_dict):
        if str_dict:
            return eval(str_dict)
        else:
            return None

    def replace_case_params(self,params)->str:
        Logger.info("替换params")
        if params and re.search("\${.*}",params):
            return self.batch_replace_variable(params)
        else:
            return params

    def replace_case_data(self,data)->str:
        Logger.info("替换data")
        if data and re.search("\${.*}",data):
            return self.batch_replace_variable(data)
        else:
            return data

    def batch_replace_variable(self,str)->str:
        vals_str = re.search("\${.*}", str).group()  # 提取出多个变量，结果如："${abc} and something else ${def}"
        pattern = r'\$\{([^}]+)\}'
        variable_list = [i for i in re.findall(pattern, vals_str)]  # 获取data中的引用变量名 列表，即 ${val} 格式中的val
        for variable in variable_list:
            str = self.replace_variable(str,variable)
        return str

    def replace_variable(self,str,variable)->str:
        _tmp = self._ly.read()
        for key in variable.split('.'):  # 例如：key=['usergoodsbrowse_index','NO_001','id']
            _tmp = _tmp[key]  # 实现循环多层取值，最后取出'id'的值
        try:
            Logger.info("替换{} 的变量 {}".format(str,variable))
            return str.replace("${"+variable+"}", _tmp)  # 字符串.replace('要被置换对象','置换后新的字符'，[，次数])
        except TypeError: #replace()进行替换时，参数值可能存在类型错误导致报错
            Logger.error("替换变量异常:{},{}".format(str,variable))

    def replace_url(self, url)->None:
        '''
        替换url中引用的变量
        '''
        Logger.info("替换url")
        if url and re.search("\${.*}",url): #两边结果都为True。(有入参url且格式正确)。用法：re.search（pattern，string，flags = 0）,search扫描整个字符串并返回第一个成功的匹配，如果没匹配到返回None。
            return self.batch_replace_variable(url)
        else:
            return url








if __name__=='__main__':
    pass





