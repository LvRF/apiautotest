class ProcessData:


    def __init__(self):
        self._ly = LoadYaml()
        self._lj = LoadJson()

    def get_module_list(self):
        # 【debug】获取excel数据 -> list
        excel_file = '../data/TestCase01.xlsx'
        ae = AnalyseExcel(excel_file)
        execl_data = ae.read_module_data()
        return execl_data

    def write_module_info(self,task_line, module_name, situation_name):
        yaml_dict = self._ly.read()

        if not yaml_dict.get('task_line',0):
            yaml_dict['task_line'] = [task_line]
        else:
            yaml_dict['task_line'].append(task_line)

        if not yaml_dict.get('module_name',0):
            yaml_dict['module_name'] = [module_name]
        else:
            yaml_dict['module_name'].append(module_name)

        if not yaml_dict.get('situation_name',0):
            yaml_dict['situation_name'] = [situation_name]
        else:
            yaml_dict['situation_name'].append(situation_name)

        self._ly.update(yaml_dict)

    def save_to_json(self, module_list) -> list:

        # 1. 将Excel数据(module_list)
        # 存储到( / data / case_data.json), 同时返回入参module_list
        with open('../data/case_data.json', 'w') as f:
            f.write(json.dumps(module_list,ensure_ascii=False))  # 另一种写法(不适合用于复杂情况，否则代码可读性差)： json.dumps(excel_data,f)
        # 2. 将业务线、模块、测试场景信息写入到配置文件(./config/field.yaml)
        for module_dict in module_list:
            self.write_module_info(module_dict['task_line'],module_dict['module_name'],module_dict['situation_name'])
        return module_list

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
        # 功能：根据excel_data 的module_code+interface_code,从json文件中获取对应用例数据 casedata
        module_list = ProcessData()._lj.read()
        for module in module_list:
            if module['module_code'].strip() == module_code:
                for interface in module['interface_list']:
                    if interface['interface_code'] == interface_code:
                        print('get_case_lists() 返回数据: ',interface['case_lists'])
                        return interface['case_lists']
                    else:
                        continue
            else:
                continue


    @staticmethod
    def get_ids(interface_code, module_code):
        # 功能：根据excel_data的module_code + interface_code, 从json文件中获取对应用例数据(用例名称、人员等相关打印信息)

        # 24/12/10 比如有两个用例时返回的列表格式：['usergoodsfavor_cancel;post;商品收藏取消操作;lvmc;陈炎清;NO_001;商品收藏取消操作', 'usergoodsfavor_cancel;post;商品收藏取消操作;lvmc;陈炎清;NO_002;debug_商品收藏取消操作']
        # 返回列表内容： interface_code,interface_method,interface_name,tester,developer,case_dict["case_number"],case_dict["case_name"]
        Ids = [ ]
        module_list = ProcessData()._lj.read()
        for module in module_list:
            if module[ 'module_code' ].strip() == module_code:
                for interface_dict in module[ 'interface_list' ]:
                    if interface_dict[ 'interface_code' ] == interface_code:
                        interface_method = interface_dict.get('method', '')
                        interface_name = interface_dict.get('interface_name', '')
                        tester = interface_dict.get('tester', '')
                        developer = interface_dict.get('developer', '')
                        case_lists = interface_dict.get('case_lists', '')

                        for case_dict in case_lists:  # 【2024/12/12-已debug确定放置层次】
                            Ids.append(
                                interface_code + ';' +
                                interface_method + ';' +
                                interface_name + ';' +
                                tester + ';' +
                                developer + ';' +
                                case_dict[ 'case_number' ] + ';' +
                                case_dict[ 'case_name' ]
                            )
        print('【debug】获取用例 Ids 成功。')
        return Ids

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
            self._ly.write(yaml_dict)
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
                target = field.split('.')[-1]
                try:
                    field_value = jsonpath.jsonpath(response,'$..{}'.format(target))
                except AttributeError:
                    Logger.info("依赖字段提取失败，返回内容异常：{}".format(response))
                    raise
            Logger.info("依赖字段开始回写：{}:{}".format(target, field_value))
            self.write_to_yaml(self._ly.read(),interface_code,case_number,target,field_value)
            Logger.info("回写后的yaml内容：{}".format(self._ly.read()))

    def replace_variable(self,str,variable)->str:
        _tmp = self._ly.read()
        for key in variable.split('.'):  # 例如：key=['usergoodsbrowse_index','NO_001','id']
            _tmp = _tmp[key]  # 实现循环多层取值，最后取出'id'的值
        try:
            Logger.info("替换{} 的变量 {}".format(str,variable))
            return str.replace("${"+variable+"}", _tmp)  # 字符串.replace('要被置换对象','置换后新的字符'，[，次数])
        except TypeError: #replace()进行替换时，参数值可能存在类型错误导致报错
            Logger.error("替换变量异常:{},{}".format(str,variable))

    def batch_replace_variable(self,str)->str:
        vals_str = re.search("\${.*}", str).group()  # 提取出多个变量，如："${abc} and something else ${def}"
        pattern = r'\$\{([^}]+)\}'
        variable_list = [ i for i in re.findall(pattern, vals_str) ]  # 获取data中的引用变量名 列表，即 ${val} 格式中的val
        for variable in variable_list:
            str = self.replace_variable(str,variable)
        return str

    def replace_case_data(self,data)->str:
        Logger.info("替换data")
        if data and re.search("\${.*}",data):
            return self.batch_replace_variable(data)
        else:
            return data

    def replace_case_params(self,params)->str:
        Logger.info("替换params")
        if params and re.search("\${.*}",params):
            return self.batch_replace_variable(params)
        else:
            return params

    def str2_dict(self,str_dict):
        if str_dict:
            return eval(str_dict)
        else:
            return None

    def adapt_case_data(self,case_data):
        # 格式化用例数据(data、params)为标准dict数据
        '''
        【思路 24/12/15】
        1、首先知道case_data用例数据中，data为带 $ 符号的字符串、params为null。
        2、「问题1」：直接使用 eval(str) 去尝试转换字符串为字典会 「语法错误」，因为 eval 函数会按照 Python 的语法规则去解析字符串内容，而字符串里的 $ 并不是 Python 语法中合法的字典键值对里的部分。
            「解决方案」：此处 $ 用于传参，故可将变量替换成对应值，再格式化处理。
        3、「问题2」：用例数据中含有 null 会报错。--因为Python 中没有名为 Null 的类型，与之类似的是 None。--故需将其进行替换。
        '''
        for case_dict in case_data:
            print("格式化case_data {}".format(case_data))
            case_dict['data'] = self.str2_dict(self.replace_case_data(case_dict['data']))
            case_dict['params'] = self.str2_dict(self.replace_case_data(case_dict['params']))

    def decorator_case(self,func):
        '''
        功能：请求前入参处理；请求后响应数据回填。 此处入参func为模板中，进行接口请求的函数(即测试用例函数)
        1、模板-请求前入参：interface_code、module_code、url、method、headers
            ---1)入参值处理：其中url值中含有变量，需要替换后才能用于请求。 2)、入参值格式处理：可能需要处理格式的字段有data/params-->封装处理 adapt_case_data()
        2、模板-请求后，通过将响应字段回填-->封装处理 update_output_field()
        '''
        pd = ProcessData()
        def wrapper(self,case_data): # args 同func()入参
            pd.adapt_case_data(case_data) # 格式化用例数据(data、params)为标准dict数据
            result = func(self,case_data)
            response, case_data, interface_code = result
            pd.update_output_field(response, interface_code, case_data['case_number'], case_data['output_field'])
            # 【待补充-校验处理】
        return wrapper






        # if __name__=='__main__':
#     3_模块功能思路 = ProcessData()
#     module_list = 3_模块功能思路.get_module_list()
#     tmp1 = 3_模块功能思路.save_to_json(module_list)
#     print(tmp1)